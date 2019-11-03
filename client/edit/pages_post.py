from client.edit.edit_forms import UploadImgForm
from client.edit.parsers import (pars_edu_request, pars_cv_request, pars_exp_request)
from client.edit.utility import (check_input_str, check_phone, check_home_number, check_telegram)
from client.edit.utility import (time_it, try_except)
from client.models import (Skills, Telephone, Sex, Citizenship, FamilyState, Children, City, State, Client, Education,
                           Certificate, CV, Experience, Sphere, Employment, TimeJob, TypeSalary, UserModel, Direction)


@try_except
@time_it
def edit_page_post(client_instance, request):  # TeamRome
    """ views.py ClientEditMain(TemplateView) POST method. """
    """ Входные данные для сохранения: """
    user = request.user
    user_name = check_input_str(request.POST['client_first_name'])
    last_name = check_input_str(request.POST['client_last_name'])
    patronymic = check_input_str(request.POST['client_middle_name'])
    sex = Sex.objects.get(sex_word=request.POST['sex']) if request.POST['sex'] else None
    date = request.POST['date_born'] if request.POST['date_born'] else None
    citizenship = Citizenship.objects.get(country_word=request.POST['citizenship']) if request.POST[
        'citizenship'] else None
    family_state = FamilyState.objects.get(state_word=request.POST['family_state']) if request.POST[
        'family_state'] else None
    children = Children.objects.get(children_word=request.POST['children']) if request.POST['children'] else None
    country = Citizenship.objects.get(country_word=request.POST['country']) if request.POST['country'] else None
    city = City.objects.get(city_word=request.POST['city']) if request.POST['city'] else None
    street = check_input_str(request.POST['street'])
    house = check_home_number(request.POST['house'])
    flat = check_home_number(request.POST['flat'])
    telegram_link = check_telegram(request.POST['telegram_link'])
    skype = check_input_str(request.POST['skype_id'])
    email = request.POST['email']
    link_linkedin = request.POST['link_linkedin']
    state = State.objects.get(state_word=request.POST['state']) if request.POST['state'] else None
    # print(user_name, last_name, patronymic, sex, date, citizenship, family_state, children, country, city,
    #       street, house, flat, telegram_link, skype, email, link_linkedin, state)

    if not client_instance:
        """ Если карточки нету - создаём. """
        print('\tUser Profile DO NOT exists - creating!')

        client = Client(
            user_client=user,
            patronymic=patronymic,
            sex=sex,
            date_born=date,
            citizenship=citizenship,
            family_state=family_state,
            children=children,
            country=country,
            city=city,
            street=street,
            house=house,
            flat=flat,
            telegram_link=telegram_link,
            skype=skype,
            link_linkedin=link_linkedin,
            state=state,
        )
        client.save()
    else:
        """ Если карточка есть - достаём из БД Объект = Клиент_id.
        Перезаписываем (изменяем) существующие данныев. """
        print('\tUser Profile exists - Overwriting user data')

        user_model = UserModel.objects.get(id=client_instance.user_client_id)
        user_model.first_name = user_name
        user_model.last_name = last_name
        user_model.email = email
        user_model.save()

        client = client_instance
        client.name = user_name
        client.last_name = last_name
        client.patronymic = patronymic
        client.sex = sex
        client.date_born = date
        client.citizenship = citizenship
        client.family_state = family_state
        client.children = children
        client.country = country
        client.city = city
        client.street = street
        client.house = house
        client.flat = flat
        client.telegram_link = telegram_link
        client.skype = skype
        client.email = email
        client.link_linkedin = link_linkedin
        client.state = state
        client.save()

    """ Сохранение телефонных номеров клиента """
    tel = request.POST.getlist('phone')
    if any(tel):
        Telephone.objects.filter(client_phone=client_instance).delete()
    for t in tel:
        t = check_phone(t)
        if t:
            phone = Telephone(
                client_phone=client,
                telephone_number=t,
            )
            phone.save()


@try_except
@time_it
def skills_page_post(client_instance, request):  # TeamRome
    """" views.py ClientEditSkills(TemplateView) POST method.  """
    skills_arr = request.POST.getlist('skill') if request.POST.getlist('skill') else None

    if any(skills_arr):
        Skills.objects.filter(client_skills=client_instance).delete()
        # print("\tskill: %s" % skills_arr)
        for s in skills_arr:
            if s:
                """ ОБЪЕДИНЕНИЕ модуля Навыки с конкретным залогиненым клиентом!!! """
                skill = Skills(
                    client_skills=client_instance,
                    skill=check_input_str(s, False)
                )
                skill.save()
    else:
        print("\tNo skills")


@try_except
@time_it
def photo_page_post(client_instance, request):  # TeamRome
    """" views.py ClientEditPhoto(TemplateView) POST method.
    В БД сохраняется УНИКАЛЬНОЕ имя картинки (пр: user_2_EntrmQR.png) в папке MEDIA_URL = '/media/' """
    form = UploadImgForm(request.POST, request.FILES)
    if form.is_valid():
        img = form.cleaned_data.get('img')
        client_instance.img = img
        client_instance.save()


@try_except
@time_it
def education_page_post(client_instance, request):  # TeamRome
    """" views.py ClientEditEducation(TemplateView) POST method.  """
    arr_edu = pars_edu_request(request.POST, request.FILES)  # list of dictionaries

    if any(arr_edu):
        Education.objects.filter(client_edu=client_instance).delete()
        for edus in arr_edu:
            if any(edus.values()):

                institution = edus['institution']
                subject_area = edus['subject_area']
                specialization = edus['specialization']
                qualification = edus['qualification']
                date_start = edus['date_start']
                date_end = edus['date_end']
                cert_arr = edus['certificate']

                education = Education(
                    client_edu=client_instance,
                    institution=institution,
                    subject_area=subject_area,
                    specialization=specialization,
                    qualification=qualification,
                    date_start=date_start,
                    date_end=date_end,
                )
                education.save()

                for c in cert_arr:  # array of tuples
                    certificate = Certificate(
                        education=education,
                        img=c[1],
                        link=c[0],
                    )
                    certificate.save()

                # print("\tEducation Form - OK:\n\t", institution, subject_area, specialization, qualification,
                #       date_start, date_end, cert_arr)
            else:
                print('\tEducation Form is Empty')
    else:
        print('\tEducation Parser is Empty')


@try_except
@time_it
def cv_page_post(client_instance, request):  # TeamRome
    """" views.py ClientEditCv(TemplateView) POST method. """
    if client_instance:
        arr_cv = pars_cv_request(request.POST)  # list of dictionaries

        if any(arr_cv):
            CV.objects.filter(client_cv=client_instance).delete()

            for cvs in arr_cv:
                position = cvs['position']
                employment = Employment.objects.get(employment=cvs['employment'])
                time_job = TimeJob.objects.get(time_job_word=cvs['time_job'])
                salary = cvs['salary']
                type_salary = TypeSalary.objects.get(type_word=cvs['type_salary'])
                direction = Direction.objects.get(id=cvs['direction'])

                if any(cvs.values()):
                    cv = CV(
                        client_cv=client_instance,
                        direction=direction,
                        position=position,
                        employment=employment,
                        time_job=time_job,
                        salary=salary,
                        type_salary=type_salary,
                    )
                    cv.save()
                    # print("\tCV Form - OK:\n\t", position, employment, time_job, salary, type_salary)
                else:
                    print('\tCv form is Empty')
        else:
            print('\tCV Parser is Empty')
    else:
        print('\tclient_instance = None!')

@try_except
@time_it
def experience_page_post(client_instance, request):  # TeamRome
    """" views.py ClientEditExperience(TemplateView) POST method. """
    arr = pars_exp_request(request.POST)  # list of dictionaries

    if any(arr):
        """ Delete old data for this client. Bug fix for duplicate date save. """
        Experience.objects.filter(client_exp=client_instance).delete()
        for dic in arr:
            if any(dic.values()):
                """ If this dictionary hes any values? than take them and save to Exp. instance. """
                organisation = dic['experience_1']
                position = dic['experience_3']
                start_date = dic['exp_date_start']
                end_date = dic['exp_date_end']
                duties = dic['experience_4']

                experiences = Experience(
                    client_exp=client_instance,
                    name=organisation,
                    position=position,
                    start_date=start_date,
                    end_date=end_date,
                    duties=duties,
                )
                experiences.save()

                spheres = dic['experience_2']
                for s in spheres:
                    if s:
                        """ Save ManyToManyField 'sphere' """
                        sp = Sphere.objects.get(id=s)
                        sp.save()
                        experiences.sphere.add(sp)

                # print("\tExperience Form - OK:\n\t", organisation, spheres, position, start_date, end_date, duties)
            else:
                print('\tExperience Form is Empty')
    else:
        print('\tExperience Parser is Empty')


@try_except
@time_it
def form_edu_post(client_instance, request):  # TeamRome
    print("FormEducation.POST: %s" % request.POST)
    form_set_edu = EducationFormSet(request.POST)
    form_set_cert = CertificateFormSet(request.POST, request.FILES)

    edu_inst = None
    if form_set_edu.is_valid():
        print('FormSet_Edu - OK')
        for f in form_set_edu:
            f_items = f.cleaned_data.items()
            print("edu_items: %s" % f_items)
            if f_items:
                """ edu_inst - unsaved model instance!
                It gives you ability to attach data to the instance before saving to the DB! """
                edu_inst = f.save(commit=False)
                """ attach ForeignKey == Client instance """
                edu_inst.client_edu = client_instance
                """ Save Education instance """
                edu_inst.save()
    else:
        print("FormSet_Edu not Valid")

    if form_set_cert.is_valid():
        print("FormSet_Cert - OK")
        for c in form_set_cert:
            c_items = c.cleaned_data.items()
            print('cert_items: %s' % c_items)
            if c_items:
                cert_inst = c.save(commit=False)
                """ attach ForeignKey == Education instance """
                cert_inst.education = edu_inst
                cert_inst.save()
    else:
        print("FormSet_Cert not Valid")
