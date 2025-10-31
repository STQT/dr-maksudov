"""
Management command to populate database with demo data for urologist
Usage: python manage.py populate_demo_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from datetime import date, timedelta
from core.models import (
    Profile, Service, Publication, Project, BlogPost,
    Achievement, Testimonial, Book
)


class Command(BaseCommand):
    help = 'Populate database with demo data for urologist in RU, UZ (Lotin) and UZ (Cyrl)'

    def add_translations(self):
        """Add translations after creating objects"""
        self.stdout.write(self.style.SUCCESS('\n📝 Adding translations...'))
        
        # Get created objects
        profile = Profile.objects.first()
        
        if profile:
            # Profile translations
            profile.full_name_uz = "Maksudov Abdurrahmon Abdullayevich"
            profile.education_uz = "Toshkent tibbiyot akademiyasi, shifokorlik fakulteti, 1998. Urologiya bo'yicha mutaxassislik, 2000."
            profile.bio_uz = '''Maksudov Abdurrahmon Abdullayevich - eng yuqori toifali vrach-urolog, tibbiyot fanlari doktori. 
                      O'zbekistonda urologiya, andrologiya va bolalar urologiyasi sohasidagi yetakchi mutaxassis.
                      
                      25 yildan ortiq ish tajribasi. Toshkent tibbiyot akademiyasi professori.
                      Urologiya bo'yicha 80 dan ortiq ilmiy nashr va 3 monografiya muallifi.
                      Evropa urologlar uyushmasi (EAU) va Xalqaro urologlar uyushmasi a'zosi.
                      
                      Urologik kasalliklarni kam invaziv usullar bilan davolash bilan shug'ullanadi,
                      jumladan endoskopik jarrohlik, laparoskopiya va lazer terapiyasi.'''
            profile.specialization_uz = "Urologiya, andrologiya, bolalar urologiyasi, onkourologiya"
            profile.address_uz = "Toshkent, O'zbekiston"
            profile.clinic_name_uz = "Urologiya va andrologiya markazi"
            profile.clinic_address_uz = "Toshkent, Amir Temur ko'chasi, 30"
            profile.working_hours_uz = "Du-Ju: 09:00 - 18:00, Sh: 09:00 - 14:00"
            profile.save()
            self.stdout.write(self.style.SUCCESS('✓ Profile translations added'))
        
        # Services translations
        services = Service.objects.all()
        for service in services:
            if 'Консультация' in service.title:
                service.title_uz = "Urolog konsultatsiyasi"
                service.description_uz = "Birinchi qabul va urologik kasalliklar bo'yicha maslahat, diagnostika va davolash rejasini tuzish"
            elif 'простатит' in service.title.lower():
                service.title_uz = "Prostatit davolash"
                service.description_uz = "O'tkir va surunkali prostatitni zamonaviy usullar bilan kompleks davolash, individual yondashuv"
            elif 'эректильная' in service.title.lower():
                service.title_uz = "Erektil disfunktsiyani davolash"
                service.description_uz = "Erektsiya buzilishlarini diagnostika va davolash, individual terapiya tanlash"
            elif 'мочекаменная' in service.title.lower():
                service.title_uz = "Tosh kasalligini davolash"
                service.description_uz = "Tosh kasalligini diagnostika va davolash, kam invaziv usullar (lazerli tosh sindirish)"
            elif 'недержание' in service.title.lower():
                service.title_uz = "Siydik tuta olmaslik davolash"
                service.description_uz = "Erkaklar va ayollarda siydik tuta olmaslikni konservativ va jarrohlik davolash"
            elif 'Диагностика' in service.title:
                service.title_uz = "Urologik kasalliklarni diagnostika qilish"
                service.description_uz = "USG, urografiya, sitoskopiya, laboratoriya diagnostikasi. To'liq kompleks tekshiruv"
            service.save()
        self.stdout.write(self.style.SUCCESS(f'✓ {services.count()} Services translations added'))

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate demo data for urologist...'))

        # Create Profile
        if not Profile.objects.exists():
            profile = Profile.objects.create(
                full_name='Максудов Абдурахман Абдуллаевич',
                birth_date=date(1975, 8, 20),
                education='Ташкентская медицинская академия, лечебный факультет, 1998. Специализация по урологии, 2000.',
                academic_degree='Доктор медицинских наук',
                academic_title='Профессор',
                bio='''Максудов Абдурахман Абдуллаевич - врач-уролог высшей категории, доктор медицинских наук. 
                       Ведущий специалист в области урологии, андрологии и детской урологии в Узбекистане.
                       
                       Опыт работы более 25 лет. Профессор Ташкентской медицинской академии.
                       Автор более 80 научных публикаций и 3 монографий по урологии.
                       Член Европейской ассоциации урологов (EAU) и Международной ассоциации урологов.
                       
                       Специализируется на малоинвазивных методах лечения урологических заболеваний,
                       включая эндоскопическую хирургию, лапароскопию и лазерную терапию.''',
                specialization='Урология, андрология, детская урология, онкоурология',
                experience_years=25,
                languages='Русский, Узбекский, Английский',
                email='maksudov.abdur@example.com',
                phone='+998 90 123 45 67',
                address='Ташкент, Узбекистан',
                clinic_name='Центр урологии и андрологии',
                clinic_address='Ташкент, ул. Амира Темура, 30',
                working_hours='Пн-Пт: 09:00 - 18:00, Сб: 09:00 - 14:00',
                telegram='https://t.me/dr_maksudov',
                facebook='https://facebook.com/dr.maksudov',
                instagram='https://instagram.com/dr.maksudov',
                linkedin='https://linkedin.com/in/maksudov-abdur'
            )
            self.stdout.write(self.style.SUCCESS('✓ Profile created'))
        else:
            self.stdout.write(self.style.WARNING('Profile already exists'))

        # Create Services
        services_data = [
            {
                'title': 'Консультация уролога',
                'description': 'Первичный прием и консультация по вопросам урологических заболеваний, диагностика и составление плана лечения',
                'duration': '30-45 мин',
                'icon': 'fas fa-user-doctor',
                'order': 1
            },
            {
                'title': 'Лечение простатита',
                'description': 'Комплексное лечение острого и хронического простатита современными методами с индивидуальным подходом',
                'duration': 'от 2 недель',
                'icon': 'fas fa-thermometer',
                'order': 2
            },
            {
                'title': 'Лечение эректильной дисфункции',
                'description': 'Диагностика и лечение нарушений эрекции, подбор индивидуальной терапии',
                'duration': 'от 1 месяца',
                'icon': 'fas fa-heartbeat',
                'order': 3
            },
            {
                'title': 'Лечение мочекаменной болезни',
                'description': 'Диагностика и лечение мочекаменной болезни, малоинвазивные методы (лазерное дробление камней)',
                'duration': '1-2 дня',
                'icon': 'fas fa-stone',
                'order': 4
            },
            {
                'title': 'Лечение недержания мочи',
                'description': 'Консервативное и хирургическое лечение недержания мочи у мужчин и женщин',
                'duration': 'от 3 дней',
                'icon': 'fas fa-shield-alt',
                'order': 5
            },
            {
                'title': 'Диагностика урологических заболеваний',
                'description': 'УЗИ, урография, цистоскопия, лабораторная диагностика. Полный комплекс обследований',
                'duration': '1-2 часа',
                'icon': 'fas fa-microscope',
                'order': 6
            }
        ]

        for service_data in services_data:
            Service.objects.get_or_create(
                title=service_data['title'],
                defaults=service_data
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(services_data)} Services created'))

        # Create Publications
        publications_data = [
            {
                'title': 'Современные методы лечения хронического простатита',
                'publication_type': 'article',
                'authors': 'Максудов А.А., Нурматов И.Р.',
                'year': 2024,
                'journal': 'Урология Узбекистана',
                'volume': '3',
                'pages': '45-58',
                'doi': '10.12345/urology.uz.2024.3.45',
                'abstract': 'Статья посвящена современным подходам к диагностике и лечению хронического простатита...',
                'keywords': 'простатит, лечение, урология',
                'citation_count': 8,
                'is_featured': True
            },
            {
                'title': 'Малоинвазивная хирургия в урологии: руководство для практикующих врачей',
                'publication_type': 'book',
                'authors': 'Максудов А.А.',
                'year': 2023,
                'publisher': 'Медицинское издательство',
                'pages': '456',
                'isbn': '978-5-02-040789-4',
                'abstract': 'Монография описывает современные малоинвазивные методы хирургического лечения урологических заболеваний...',
                'keywords': 'хирургия, урология, малоинвазивные методы',
                'is_featured': True
            },
            {
                'title': 'Эндоскопическое лечение мочекаменной болезни',
                'publication_type': 'article',
                'authors': 'Максудов А.А., Каримов Д.Т.',
                'year': 2023,
                'journal': 'Азиатский журнал урологии',
                'volume': '15',
                'pages': '120-135',
                'doi': '10.12345/ajur.2023.15.120',
                'abstract': 'Исследование эффективности эндоскопических методов лечения мочекаменной болезни...',
                'keywords': 'мочекаменная болезнь, эндоскопия, лечение',
                'citation_count': 15,
                'is_featured': True
            }
        ]

        for pub_data in publications_data:
            Publication.objects.get_or_create(
                title=pub_data['title'],
                defaults=pub_data
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(publications_data)} Publications created'))

        # Create Projects (Clinical Cases)
        projects_data = [
            {
                'title': 'Внедрение лапароскопической хирургии в урологию',
                'description': 'Разработка и внедрение современных лапароскопических методов лечения урологических заболеваний',
                'start_date': date(2022, 1, 1),
                'end_date': date(2024, 12, 31),
                'role': 'Руководитель клинического проекта',
                'organization': 'Центр урологии и андрологии',
                'funding': 'Министерство здравоохранения Узбекистана',
                'results': 'Проведено 150+ успешных лапароскопических операций',
                'order': 1
            },
            {
                'title': 'Региональная программа по ранней диагностике рака простаты',
                'description': 'Организация скрининговых программ для раннего выявления рака предстательной железы',
                'start_date': date(2024, 3, 1),
                'end_date': None,
                'role': 'Главный координатор',
                'organization': 'Онкологический центр',
                'funding': 'ВОЗ, Global Cancer Alliance',
                'results': 'Обследовано более 5000 пациентов',
                'is_active': True,
                'order': 2
            }
        ]

        for project_data in projects_data:
            Project.objects.get_or_create(
                title=project_data['title'],
                defaults=project_data
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(projects_data)} Projects created'))

        # Create Blog Posts
        blog_posts_data = [
            {
                'title': 'Профилактика простатита: важные советы для мужчин',
                'slug': 'profilaktika-prostatita',
                'excerpt': 'Узнайте, как защитить себя от простатита: простые советы по профилактике и раннему выявлению',
                'category': 'Профилактика',
                'tags': 'простатит, профилактика, мужское здоровье, урология',
                'is_published': True,
                'published_at': timezone.now() - timedelta(days=5)
            },
            {
                'title': 'Эректильная дисфункция: современные методы лечения',
                'slug': 'erektilnaya-disfunkciya-lechenie',
                'excerpt': 'Современные методы диагностики и лечения эректильной дисфункции: от медикаментозной терапии до хирургии',
                'category': 'Лечение',
                'tags': 'эректильная дисфункция, лечение, андрология, мужское здоровье',
                'is_published': True,
                'published_at': timezone.now() - timedelta(days=12)
            },
            {
                'title': 'Мочекаменная болезнь: от диагностики до лечения',
                'slug': 'mochekamennaya-bolezn',
                'excerpt': 'Диагностика и современные методы лечения мочекаменной болезни: от консервативной терапии до хирургии',
                'category': 'Лечение',
                'tags': 'мочекаменная болезнь, камни в почках, лечение, урология',
                'is_published': True,
                'published_at': timezone.now() - timedelta(days=20)
            }
        ]

        for blog_data in blog_posts_data:
            BlogPost.objects.get_or_create(
                slug=blog_data['slug'],
                defaults=blog_data
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(blog_posts_data)} Blog posts created'))

        # Create Achievements
        achievements_data = [
            {
                'title': 'Почетная грамота Министерства здравоохранения',
                'description': 'За выдающийся вклад в развитие урологии Узбекистана',
                'date': date(2023, 12, 15),
                'organization': 'Министерство здравоохранения Узбекистана',
                'order': 1
            },
            {
                'title': 'Лучший уролог года',
                'description': 'Премия Ассоциации урологов Узбекистана за лучшие результаты в лечении',
                'date': date(2024, 5, 20),
                'organization': 'Ассоциация урологов Узбекистана',
                'order': 2
            },
            {
                'title': 'Сертификат EAU (European Association of Urology)',
                'description': 'Международная сертификация по эндоскопической урологии',
                'date': date(2023, 6, 10),
                'organization': 'European Association of Urology',
                'order': 3
            }
        ]

        for achievement_data in achievements_data:
            Achievement.objects.get_or_create(
                title=achievement_data['title'],
                defaults=achievement_data
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(achievements_data)} Achievements created'))

        # Create Testimonials
        testimonials_data = [
            {
                'patient_name': 'Рахимов Аброр Абдуллаевич',
                'patient_age': 45,
                'text': 'Профессиональный врач с большим опытом. Лечился от простатита - результат отличный, теперь чувствую себя здоровым! Рекомендую всем.',
                'rating': 5,
                'is_approved': True
            },
            {
                'patient_name': 'Каримов Шухрат Темирович',
                'patient_age': 52,
                'text': 'Выражаю огромную благодарность доктору Максудову! Лазерное дробление камня прошло без осложнений, восстановился быстро.',
                'rating': 5,
                'is_approved': True
            },
            {
                'patient_name': 'Хасанов Дилшод Улугбекович',
                'patient_age': 38,
                'text': 'Обратился с проблемой эректильной дисфункции. Благодаря грамотному лечению проблема решена. Спасибо за профессионализм!',
                'rating': 5,
                'is_approved': True
            },
            {
                'patient_name': 'Нурматов Икром Баходирович',
                'patient_age': 55,
                'text': 'Очень доволен результатами лечения. Внимательный врач, современное оборудование, квалифицированный персонал.',
                'rating': 5,
                'is_approved': True
            }
        ]

        for testimonial_data in testimonials_data:
            Testimonial.objects.get_or_create(
                patient_name=testimonial_data['patient_name'],
                defaults=testimonial_data
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(testimonials_data)} Testimonials created'))

        # Create Books
        books_data = [
            {
                'title': 'Современная урология: от диагностики до лечения',
                'slug': 'sovremennaya-urologiya',
                'author': 'Максудов А.А.',
                'short_description': 'Комплексное руководство по современной урологии с практическими рекомендациями',
                'publisher': 'Медицинское издательство',
                'publication_year': 2023,
                'isbn': '978-5-02-040123-5',
                'pages': 672,
                'language': 'Русский',
                'price': '150000',
                'is_available': True,
                'is_featured': True,
                'order': 1
            },
            {
                'title': 'Эндоскопическая урология: практическое руководство',
                'slug': 'endoskopicheskaya-urologiya',
                'author': 'Максудов А.А., Каримов Д.Т.',
                'short_description': 'Практическое руководство по эндоскопическим методам в урологии',
                'publisher': 'Институт последипломного образования',
                'publication_year': 2024,
                'isbn': '978-5-9916-5678-0',
                'pages': 480,
                'language': 'Русский',
                'price': '120000',
                'is_available': True,
                'is_featured': True,
                'order': 2
            },
            {
                'title': 'Андрология: диагностика и лечение мужских заболеваний',
                'slug': 'andrologiya-diagnostika-lechenie',
                'author': 'Максудов А.А.',
                'short_description': 'Комплексный подход к диагностике и лечению мужских урологических заболеваний',
                'publisher': 'Медицинское издательство',
                'publication_year': 2023,
                'isbn': '978-5-02-040789-6',
                'pages': 384,
                'language': 'Русский',
                'price': '100000',
                'is_available': True,
                'is_featured': False,
                'order': 3
            }
        ]

        for book_data in books_data:
            Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(books_data)} Books created'))

        # Add translations
        self.add_translations()

        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✅ Demo data for urologist successfully populated!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('\n📊 Statistics:'))
        self.stdout.write(self.style.SUCCESS(f'   • Profile: 1'))
        self.stdout.write(self.style.SUCCESS(f'   • Services: {len(services_data)}'))
        self.stdout.write(self.style.SUCCESS(f'   • Publications: {len(publications_data)}'))
        self.stdout.write(self.style.SUCCESS(f'   • Projects: {len(projects_data)}'))
        self.stdout.write(self.style.SUCCESS(f'   • Blog Posts: {len(blog_posts_data)}'))
        self.stdout.write(self.style.SUCCESS(f'   • Achievements: {len(achievements_data)}'))
        self.stdout.write(self.style.SUCCESS(f'   • Testimonials: {len(testimonials_data)}'))
        self.stdout.write(self.style.SUCCESS(f'   • Books: {len(books_data)}'))
        self.stdout.write(self.style.SUCCESS('\n🌐 You can now:'))
        self.stdout.write(self.style.SUCCESS('1. Visit http://127.0.0.1:8000'))
        self.stdout.write(self.style.SUCCESS('2. Visit admin at http://127.0.0.1:8000/admin'))
        self.stdout.write(self.style.SUCCESS('3. Browse services, publications, and blog'))
