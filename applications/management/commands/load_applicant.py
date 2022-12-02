from django.core.management.base import BaseCommand
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
import re
from collections import namedtuple
import time
import requests
from applications.models import Application, Transaction
from applications.utils import generate_roll_no
from call_applications.models import CallForApplication
from profiles.models import AchievementMembership, BasicInfo, EducationalBackground, TestScore, WorkExperience
from profiles.serializers import ProfileSerializer
from user.models import User
import random
import dateutil.parser 

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

client_secret_file = os.path.join(os.path.dirname(__file__), '_client_secret.json')
random_words = ["dingmaul","daymares","blipping","uncasked","pickpole",
        "sellaite","snooking","brambles","deporter","etherean","rebutter",
        "allelism","anodizes","schlepps","belledom","placebos","shortish",
        "enactory","delphine","subtrude","unglossy","grimines","apocrita","gelasian",
        "levering","assailer","trichion","jacolatt","limewort","ancodont",
        "likeways","ropework","wellmost","homodyne","testamur","timbered",
        "clumping","bryaceae","siziness","sentried","cowheart","dioramic",
        "largeous","plateman","vowelism","pulvinni","outsulks","orphancy","adenosis",
        "clicking","weregild","aminosis","chancing","unportly","foreview",
        "beadings","jeremiad","immotile","outgleam","carucate"
        ]

static_proxies = [
    {"https": "http://vqdytdhy:tctgyaae8lc2@45.87.243.225:6227"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@95.164.135.47:6580"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@192.186.151.141:8642"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@69.58.9.16:7086"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@170.244.92.70:8630"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@45.86.66.217:6470"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@171.22.133.7:7266"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@144.168.145.8:6056"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@185.101.169.253:6797"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@138.128.69.4:8073"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@94.131.81.81:6221"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@104.144.3.98:6177"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@23.236.183.33:8604"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@144.168.140.29:8100"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@23.236.183.152:8723"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@209.127.183.32:8130"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@107.152.190.209:7230"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@104.223.223.77:6662"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@84.21.189.226:5873"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@104.144.147.150:8184"},
    {"https": "http://vqdytdhy:tctgyaae8lc2@107.152.170.63:9114"},
]


def direct_google_drive_link_generator(link):
    d_id = link.split('id=')[-1]
    return "https://drive.google.com/uc?export=download&id={}".format(d_id)

class Command(BaseCommand):
    help = 'Loads Applicants information from google sheet'

    def handle(self, *args, **options):

        open_applications = CallForApplication.objects.all()
        
        options = {i: open_applications[i].title for i in range(len(open_applications))}
        print(options)
        choice = input("Select season to load applicant. only integer number: ")
        try:
            open_application = open_applications[int(choice)]
        except:
            print("Something went wrong")
            return

        sheet_link = input("Please insert the google sheet file url: ")
        # sheet_link = 'https://docs.google.com/spreadsheets/d/1GaH7uxtoa6dg4-M7gl-wDqWhGsozCuKfG680NR7ZALs/edit?usp=sharing'
        scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret_file, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(sheet_link).sheet1
        
        print(sheet)
        list_of_lists = sheet.get_all_values()
        headers = list_of_lists[0]

        user = {"email": "", "gender": "", "date_of_birth": "", "full_name": ""}
        basic_info = {
            "father_name": "", "mother_name": "", "nationality": "",
            "nid_passport_no": "", "is_employed": "", "permanent_address": "",
            "present_address": "", "phone_number": "", "work_phone": "",
            "photo" : "",
        }
        test_scores = []
        achievement_memberships = []
        work_experiences = []
        educations = []


        matched_index = {}

        i = 0 
        while i < len(headers):
            header = headers[i]
            title = re.sub(r'\d.', "", header).strip().lower()

            if title == "name":
                matched_index["full_name"] = i
            if "email" in title:
                matched_index["email"] = i
            elif "mother" in title:
                matched_index["mother_name"] = i
            elif "father" in title:
                matched_index["father_name"] = i
            elif "birth" in title:
                matched_index["date_of_birth"] = i
            elif "photo" in title:
                matched_index["photo"] = i
            elif "nationality" in title:
                matched_index["nationality"] = i
            elif "national id" in title:
                matched_index["nid_passport_no"] = i
            elif "gender" in title:
                matched_index["gender"] = i
            elif "employed" in title:
                matched_index["is_employed"] = i
            elif "permanent" in title:
                matched_index["permanent_address"] = i
            elif "present" in title:
                matched_index["present_address"] = i
            elif "mobile number" in title:
                matched_index["phone_number"] = i
            elif "work phone" in title:
                matched_index["work_phone"] = i
            elif "transaction id" in title:
                matched_index["transaction_id"] = i
            elif "transaction date" in title:
                matched_index["transaction_time"] = i
            elif "payment information ( phone number)" in title:
                matched_index["transaction_from"] = i

            elif "academic" in title:
                j = len(matched_index.get("educations", []))
                print(j)
                if j == 0:
                    matched_index["educations"] = [{}]
                else:
                    matched_index["educations"].append({})
                matched_index["educations"][j]["degree"] = i
                matched_index["educations"][j]["institute"] = i + 1
                matched_index["educations"][j]["passing_year"] = i + 2
                matched_index["educations"][j]["area_major"] = i + 3
                matched_index["educations"][j]["division_class_cgpa"] = i + 4
                i = i + 5
                continue
            elif "work experience" in title:
                
                j = len(matched_index.get("work_experiences", []))
                print(j)

                if j == 0:
                    matched_index["work_experiences"] = [{}]
                else:
                    matched_index["work_experiences"].append({})
                matched_index["work_experiences"][j]["post"] = i
                matched_index["work_experiences"][j]["organization"] = i + 1
                matched_index["work_experiences"][j]["major_responsibilities"] = i + 2
                matched_index["work_experiences"][j]["from_to"] = i + 3
                i = i + 4
                continue
                
            elif "score" in title:
                j = len(matched_index.get("test_scores", []))
                print(j)

                if j == 0:
                    matched_index["test_scores"] = [{}]
                else:
                    matched_index["test_scores"].append({}) 
                matched_index["test_scores"][j]["test_score"] = i
                matched_index["test_scores"][j]["test_date"] = i + 1
                i = i + 2
                continue
            
            elif "achievements" in title:
                j = len(matched_index.get("achievement_memberships", []))
                print(j)

                if j == 0:
                    matched_index["achievement_memberships"] = [{}]
                else:
                    matched_index["achievement_memberships"].append({})
                matched_index["achievement_memberships"][j]["achievement_type"] = i
                matched_index["achievement_memberships"][j]["organization"] = i + 1
                matched_index["achievement_memberships"][j]["year"] = i + 2
                i = i + 3
                continue
            i = i + 1

                                           
        for row in list_of_lists[1:]:
            # print(row.index(matched_index["full_name"]))
            user["email"] = row[matched_index["email"]]
            user["full_name"] = row[matched_index["full_name"]]
            user["gender"] = 0 if row[matched_index["gender"]].lower() == "male" else 1
            user["date_of_birth"] =dateutil.parser.parse(row[matched_index["date_of_birth"]]).date()
            
            print(user)
            basic_info["father_name"] = row[matched_index["father_name"]] 
            basic_info["mother_name"] = row[matched_index["mother_name"]] 
            basic_info["nationality"] = row[matched_index["nationality"]]
            basic_info["nid_passport_no"] = row[matched_index["nid_passport_no"]] 
            basic_info["is_employed"] = True if any(ext in row[matched_index["is_employed"]].lower() for ext in ["yes",])  else False
            basic_info["permanent_address"] = row[matched_index["permanent_address"]]
            basic_info["present_address"] = row[matched_index["present_address"]] 
            basic_info["phone_number"] = row[matched_index["phone_number"]] 
            basic_info["work_phone"] = row[matched_index["work_phone"]]
            basic_info["photo"] = row[matched_index["photo"]]
            # print(basic_info)
            
            test_scores = []
            for entry in matched_index["test_scores"]:
                test_and_score = row[entry["test_score"]]
                if "ielts" in test_and_score.lower():
                    test = "IELTS"
                    score = test_and_score.lower().replace("ielts", "").strip()
                elif "gre" in test_and_score.lower():
                    test = "GRE"
                    score = test_and_score.lower().replace("gre", "").strip()
                elif "gmat" in test_and_score.lower():
                    test = "GMAT"
                    score = test_and_score.lower().replace("gmat", "").strip()
                elif "toefl" in test_and_score.lower():
                    test = "TOEFL"
                    score = test_and_score.lower().replace("toefl", "").strip()
                else:
                    continue
                test_date = dateutil.parser.parse(row[entry["test_date"]]).date()
                test_scores.append({"test": test, "score": score, "test_date": test_date} )

            # print(test_scores)
            achievement_memberships = []
            for entry in matched_index["achievement_memberships"]:
                if "membership" in row[entry["achievement_type"]].lower():
                    achievement_type = "membership"
                elif "achieve" in row[entry["achievement_type"]].lower():
                    achievement_type = "achievement"
                elif "award" in row[entry["achievement_type"]].lower():
                    achievement_type = "award"

                organization = row[entry["organization"]]
                if not organization:
                    continue
                # test_date = dateutil.parser.parse(row[entry["year"]])

                year = row[entry["year"]].lower().replace('no', "").replace("na", "").replace('n/a', "").strip()
                achievement_memberships.append({"achievement_type": achievement_type, "organization": organization, "year": year} )

            work_experiences = []   
            for entry in matched_index["work_experiences"]:
                post = row[entry["post"]].replace('no', "").replace("na", "").replace('n/a', "").strip()
                
                organization = row[entry["organization"]].replace('no', "").replace("na", "").replace('n/a', "").strip()
                if not post or not organization:
                    continue

                major_responsibilities = row[entry["major_responsibilities"]]
                from_to = row[entry["from_to"]]

                from_date = from_to.lower().split('to')[0]
                to_date = ""
                is_current = True
                if len(from_to.lower().split('to')) > 1:
                    to_date = from_to.lower().split('to')[1].lower()
                    if  not any(ext in to_date for ext in ["continue", "present", "current", "running" ]):
                        is_current = False
                        to_date = from_to.lower().split('to')[1]
                
                work_experiences.append({"post": post, "organization": organization, "major_responsibilities": major_responsibilities,
                        "from_date": from_date, "to_date": to_date, "is_current": is_current})
            # print(work_experiences)
            
            
            educations = []   
            for entry in matched_index["educations"]:
                degree = row[entry["degree"]].replace('no', "").replace("na", "").replace('n/a', "").strip()
                
                institute = row[entry["institute"]].replace('no', "").replace("na", "").replace('n/a', "").strip()
                if not degree or not institute:
                    continue

                passing_year = row[entry["passing_year"]]
                area_major = row[entry["area_major"]]
                division_class_cgpa = row[entry["division_class_cgpa"]]

                educations.append({
                    "degree": degree,
                    "institute": institute,
                    "passing_year": passing_year,
                    "area_major":area_major,
                    "division_class_cgpa":division_class_cgpa
                })
            # print(educations)
           
            user_new = User.objects.filter(email=user["email"])
            print(basic_info["mother_name"][-3:].lower()+ user["date_of_birth"].strftime("%Y"))
            if not user_new:
                user_new = User.objects.create(email=user["email"], full_name=user["full_name"], date_of_birth=user["date_of_birth"], gender=user["gender"])
                user_new.set_password(basic_info["mother_name"].strip()[-3:].lower()+ user["date_of_birth"].strftime("%Y"))
                user_new.save()
                print("user saved successfully")
            else:
                print("User already exist")
                user_new = user_new[0]

            basic_info_new = BasicInfo.objects.filter(user=user_new)
            print(basic_info)
            if not basic_info_new:
                basic_info_new = BasicInfo.objects.create(
                    user=user_new, father_name = basic_info["father_name"], 
                    mother_name = basic_info["mother_name"], nationality = basic_info["nationality"], 
                    nid_passport_no = basic_info["nid_passport_no"], is_employed = basic_info["is_employed"], 
                    permanent_address = basic_info["permanent_address"], present_address = basic_info["present_address"], 
                    phone_number = basic_info["phone_number"], work_phone = basic_info["work_phone"] )
            else:
                basic_info_new = basic_info_new[0]
                print("basic info exist")  

            if not basic_info_new.photo: 
                link = direct_google_drive_link_generator( basic_info["photo"])
                req_headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) {}/105.0.0.0 Safari/537.36'.format(random.choice(random_words))
                }

                for i in range(3):
                    try:
                        r = requests.get(link, headers=req_headers, proxies=random.choice(static_proxies))
                        if r.status_code ==200:
                            break
                    except Exception as e:
                        print(e)
                        print("retrying")
                        
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(r.content)
                img_temp.flush()

                result = basic_info_new.photo.save("{}.jpg".format(user_new.id), File(img_temp))
                img_temp.close()

                basic_info_new.save()
                print("basic info created successfully ")
        
            if educations:
                for education in educations:
                    print(education)
                    ed =  EducationalBackground.objects.get_or_create(user=user_new, **education)
                    # ed.save()

            if work_experiences:
                for work in work_experiences:
                    print(work)
                    wx = WorkExperience.objects.get_or_create(user=user_new, **work)
                    # wx.save()
            if achievement_memberships:
                for ach in achievement_memberships:
                    print(ach)
                    am = AchievementMembership.objects.get_or_create(user=user_new, **ach)
                    # am.save()

            if test_scores:
                for test in test_scores:
                    print(test)
                    ts = TestScore.objects.get_or_create(user=user_new, **test)
                    
            transaction = Transaction.objects.get_or_create(
                                payment_type="Manual", transaction_method="Bkash", amount='500',
                                 transaction_from=row[matched_index["transaction_from"]], transaction_id=row[matched_index["transaction_id"]],
                                 transaction_time=dateutil.parser.parse(row[matched_index["transaction_time"]]).date(),
                                is_approved=True, user=user_new
                            )

            ProfileData = namedtuple('ProfileData', ('basic_info', 'test_scores', 'achievements', 'work_experiences', 'educational_backgrounds', 'user'))

            profile = ProfileData(
                basic_info=BasicInfo.objects.filter(user=user_new),
                test_scores=TestScore.objects.filter(user=user_new),
                achievements=AchievementMembership.objects.filter(user=user_new),
                work_experiences=WorkExperience.objects.filter(user=user_new),
                educational_backgrounds=EducationalBackground.objects.filter(user=user_new),
                user=user_new
            )
            profile_serializer = ProfileSerializer(profile)
        
            applications = Application.objects.filter(user=user_new, call_for_application=open_application)
            if not applications:
                application = Application.objects.create(
                    call_for_application=open_application, transaction=transaction, user=user_new, data=profile_serializer.data, is_approved=True, roll_no = generate_roll_no(open_application), is_payment_done=True  )
            else:
                print("Application already exist")
                continue
            
                