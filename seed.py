from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, UserProfile, CompanyProfile, JobCategory, Job, Application, SavedJob

def seed_database():
    app = create_app()
    with app.app_context():
        print("Recreating database tables...")
        db.drop_all()
        db.create_all()

        print("1. Seeding Job Categories...")
        categories_data = [
            {
                "name": "Software Engineering",
                "slug": "software-engineering",
                "icon_class": "bi-code-slash",
                "description": "Backend, Frontend, Full-stack, Mobile & Systems Programming roles."
            },
            {
                "name": "AI & Data Science",
                "slug": "ai-data-science",
                "icon_class": "bi-cpu",
                "description": "Machine Learning, Deep Learning, NLP, Data Engineering & Analytics."
            },
            {
                "name": "UI/UX & Product Design",
                "slug": "design-creative",
                "icon_class": "bi-palette",
                "description": "Product Designers, UI/UX Specialists, Brand & Interaction Designers."
            },
            {
                "name": "Cloud & DevOps",
                "slug": "cloud-devops",
                "icon_class": "bi-cloud-check",
                "description": "Kubernetes, CI/CD pipelines, Site Reliability & Cloud Infrastructure."
            },
            {
                "name": "Product Management",
                "slug": "product-management",
                "icon_class": "bi-kanban",
                "description": "Technical Product Managers, Group PMs & Product Owners."
            },
            {
                "name": "Marketing & Growth",
                "slug": "marketing-growth",
                "icon_class": "bi-megaphone",
                "description": "Growth Marketing, SEO, Content Strategy & Developer Relations."
            },
            {
                "name": "Cybersecurity",
                "slug": "cybersecurity",
                "icon_class": "bi-shield-check",
                "description": "Information Security, Penetration Testing & AppSec Engineering."
            },
            {
                "name": "Finance & Operations",
                "slug": "finance-operations",
                "icon_class": "bi-graph-up-arrow",
                "description": "Financial Planning, Business Operations & Strategy."
            }
        ]

        category_objs = {}
        for cat in categories_data:
            c = JobCategory(
                name=cat["name"],
                slug=cat["slug"],
                icon_class=cat["icon_class"],
                description=cat["description"]
            )
            db.session.add(c)
            category_objs[cat["slug"]] = c
        
        db.session.commit()

        print("2. Seeding Employer Accounts & Company Profiles...")
        
        # Employer 1: TechCorp
        emp1 = User(username="techcorp", email="recruiter@techcorp.com", role="employer")
        emp1.set_password("password123")
        db.session.add(emp1)
        db.session.flush()

        comp1 = CompanyProfile(
            user_id=emp1.id,
            company_name="TechCorp Global",
            tagline="Pioneering enterprise cloud and financial infrastructure",
            industry="Fintech & Cloud Systems",
            company_size="500+ employees",
            website="https://techcorp.example.com",
            location="San Francisco, CA",
            founded_year=2016,
            about="TechCorp Global is a premier financial technology organization building scalable payment gateways, banking microservices, and real-time transaction rails utilized by millions worldwide."
        )
        db.session.add(comp1)

        # Employer 2: Innovate AI
        emp2 = User(username="innovate_ai", email="careers@innovatelabs.io", role="employer")
        emp2.set_password("password123")
        db.session.add(emp2)
        db.session.flush()

        comp2 = CompanyProfile(
            user_id=emp2.id,
            company_name="Innovate AI Labs",
            tagline="Next-generation generative AI and foundational language agents",
            industry="Artificial Intelligence",
            company_size="51-200 employees",
            website="https://innovatelabs.example.io",
            location="New York, NY",
            founded_year=2022,
            about="We build advanced generative AI agents, neural retrieval engines, and high-performance inference platforms pushing the boundaries of machine intelligence."
        )
        db.session.add(comp2)

        # Employer 3: Nexus Studios
        emp3 = User(username="nexus_studios", email="talent@nexusstudios.com", role="employer")
        emp3.set_password("password123")
        db.session.add(emp3)
        db.session.flush()

        comp3 = CompanyProfile(
            user_id=emp3.id,
            company_name="Nexus Design Studio",
            tagline="Crafting delightful digital experiences and brand identities",
            industry="Design & Creative",
            company_size="11-50 employees",
            website="https://nexusstudios.example.com",
            location="Austin, TX",
            founded_year=2019,
            about="Nexus is a boutique design consultancy working with hyper-growth startups to create unforgettable product designs, design systems, and web interfaces."
        )
        db.session.add(comp3)

        db.session.commit()

        print("3. Seeding Job Postings...")
        jobs_data = [
            {
                "employer": emp1,
                "category": category_objs["software-engineering"],
                "title": "Senior Full-Stack Python Engineer",
                "job_type": "Full-time",
                "experience_level": "Senior Level",
                "location": "San Francisco, CA (or Remote)",
                "is_remote": True,
                "salary_currency": "$",
                "salary_min": 145000,
                "salary_max": 185000,
                "skills_required": "Python, Flask, React, PostgreSQL, Docker, Redis",
                "description": "We are seeking an experienced Senior Full-Stack Engineer to architect and scale our core payment processing engine. In this role, you will lead backend microservices development using Flask and modern frontend SPAs using React.",
                "requirements": "• 5+ years of experience in Python web development (Flask / Django / FastAPI)\n• Proficiency with modern JavaScript / TypeScript and React\n• Strong SQL skills and experience designing relational schemas (PostgreSQL)\n• Hands-on experience with containerization (Docker) and message queues (Redis / RabbitMQ)\n• Excellent communication skills in remote environments",
                "benefits": "• Top-tier medical, dental, and vision insurance with 100% premium coverage\n• $3,000 annual education & conference stipend\n• Flexible 100% remote work setup + $1,500 home office budget\n• 401(k) retirement match up to 5%\n• Generous stock options package",
                "deadline": datetime.utcnow() + timedelta(days=45)
            },
            {
                "employer": emp2,
                "category": category_objs["ai-data-science"],
                "title": "Machine Learning Research Engineer",
                "job_type": "Full-time",
                "experience_level": "Senior Level",
                "location": "New York, NY",
                "is_remote": False,
                "salary_currency": "$",
                "salary_min": 170000,
                "salary_max": 230000,
                "skills_required": "PyTorch, LLMs, Transformer Architecture, CUDA, Python",
                "description": "Join our cutting-edge AI research team to train, fine-tune, and optimize large-scale language models and agentic reasoning architectures for enterprise applications.",
                "requirements": "• M.S. or Ph.D. in Computer Science, Machine Learning, or equivalent quantitative discipline\n• Proven track record in training and evaluating Transformer models using PyTorch\n• Experience with distributed training frameworks (DeepSpeed / Megatron-LM)\n• Deep understanding of reinforcement learning and RLHF algorithms",
                "benefits": "• Competitive base salary + equity in high-growth AI unicorn\n• Unlimited PTO and comprehensive health coverage\n• State-of-the-art GPU computing clusters\n• Daily catered lunches in Manhattan office",
                "deadline": datetime.utcnow() + timedelta(days=30)
            },
            {
                "employer": emp3,
                "category": category_objs["design-creative"],
                "title": "Lead UI/UX Product Designer",
                "job_type": "Full-time",
                "experience_level": "Lead / Executive",
                "location": "Austin, TX (Remote OK)",
                "is_remote": True,
                "salary_currency": "$",
                "salary_min": 125000,
                "salary_max": 160000,
                "skills_required": "Figma, Design Systems, UX Research, Prototyping, Wireframing",
                "description": "Nexus Design Studio is looking for a visionary Lead Product Designer to guide product strategy, develop modular design systems, and deliver seamless user experiences for our premier clients.",
                "requirements": "• 6+ years of UI/UX product design experience with an exceptional portfolio\n• Mastery of Figma, Auto Layout, Variables, and design token architectures\n• Strong capability in conducting user interviews and usability testing\n• Experience partnering closely with frontend engineering teams",
                "benefits": "• Flexible hours and four-day workweek experiment\n• Latest MacBook Pro and top-of-the-line design software subscriptions\n• Annual team retreats in world-class destinations\n• Performance-based annual profit sharing",
                "deadline": datetime.utcnow() + timedelta(days=60)
            },
            {
                "employer": emp1,
                "category": category_objs["cloud-devops"],
                "title": "DevOps & Cloud Infrastructure Engineer",
                "job_type": "Full-time",
                "experience_level": "Mid Level",
                "location": "Seattle, WA",
                "is_remote": True,
                "salary_currency": "$",
                "salary_min": 130000,
                "salary_max": 165000,
                "skills_required": "Kubernetes, Terraform, AWS, CI/CD, Prometheus, Docker",
                "description": "Scale our cloud infrastructure supporting over 10M daily transactions. You will automate multi-region Kubernetes deployments, maintain infrastructure-as-code with Terraform, and bolster observability.",
                "requirements": "• 3+ years managing production infrastructure on AWS / GCP\n• Deep expertise with Kubernetes orchestration, Helm, and service meshes\n• Strong proficiency in Terraform and GitOps practices (ArgoCD)\n• Experience implementing zero-downtime blue/green deployment strategies",
                "benefits": "• Comprehensive health, dental, and life insurance\n• 401(k) matching and stock purchase plans\n• Remote work equipment allowance",
                "deadline": datetime.utcnow() + timedelta(days=20)
            },
            {
                "employer": emp2,
                "category": category_objs["product-management"],
                "title": "Technical Product Manager - AI Platform",
                "job_type": "Full-time",
                "experience_level": "Senior Level",
                "location": "New York, NY (Hybrid)",
                "is_remote": False,
                "salary_currency": "$",
                "salary_min": 150000,
                "salary_max": 195000,
                "skills_required": "Product Roadmapping, AI/ML APIs, Agile, User Analytics, Jira",
                "description": "Define the vision and roadmap for our developer-facing AI inference API platform. Partner with research engineers and enterprise customers to ship game-changing AI capabilities.",
                "requirements": "• 4+ years of product management experience focused on developer tools, APIs, or AI/ML systems\n• Solid understanding of software development workflows and cloud infrastructure\n• Proven ability to translate complex technical concepts into intuitive developer experiences",
                "benefits": "• Generous equity grant\n• Premium health & wellness coverage\n• Learning and conference budget",
                "deadline": datetime.utcnow() + timedelta(days=40)
            },
            {
                "employer": emp1,
                "category": category_objs["cybersecurity"],
                "title": "Senior Security & AppSec Engineer",
                "job_type": "Full-time",
                "experience_level": "Senior Level",
                "location": "San Francisco, CA",
                "is_remote": True,
                "salary_currency": "$",
                "salary_min": 160000,
                "salary_max": 200000,
                "skills_required": "Penetration Testing, OWASP, Cloud Security, Python, Cryptography",
                "description": "Protect our global financial infrastructure by conducting vulnerability assessments, implementing secure SDLC practices, and defending against advanced persistent threats.",
                "requirements": "• 5+ years of application security or penetration testing experience\n• Deep knowledge of OWASP Top 10, auth protocols (OAuth2, SAML, JWT), and cryptography\n• Relevant industry certifications (OSCP, CISSP, CEH) preferred",
                "benefits": "• Top-tier compensation & annual bonus\n• 100% remote flexibility\n• Comprehensive health package",
                "deadline": datetime.utcnow() + timedelta(days=50)
            },
            {
                "employer": emp3,
                "category": category_objs["software-engineering"],
                "title": "Frontend React & Next.js Developer",
                "job_type": "Contract",
                "experience_level": "Mid Level",
                "location": "Remote",
                "is_remote": True,
                "salary_currency": "$",
                "salary_min": 95000,
                "salary_max": 130000,
                "skills_required": "React, Next.js, TypeScript, Tailwind CSS, REST APIs",
                "description": "Build hyper-polished, responsive web applications with smooth micro-interactions and pixel-perfect UI implementation alongside our design team.",
                "requirements": "• 3+ years building production applications in React / TypeScript\n• Strong command of modern CSS (Tailwind, CSS Modules, animations)\n• Experience optimizing Core Web Vitals and performance benchmarks",
                "benefits": "• 100% flexible work schedule\n• High hourly/annual contract rate with potential for full-time conversion\n• Work on diverse, award-winning client projects",
                "deadline": datetime.utcnow() + timedelta(days=25)
            },
            {
                "employer": emp2,
                "category": category_objs["marketing-growth"],
                "title": "Technical Developer Advocate (DevRel)",
                "job_type": "Full-time",
                "experience_level": "Mid Level",
                "location": "San Francisco, CA",
                "is_remote": True,
                "salary_currency": "$",
                "salary_min": 115000,
                "salary_max": 150000,
                "skills_required": "Developer Relations, Technical Writing, Python, Public Speaking",
                "description": "Champion developer adoption of our AI SDKs through engaging tutorials, open-source sample apps, conference talks, and community hackathons.",
                "requirements": "• 2+ years experience in developer relations, developer marketing, or software engineering\n• Ability to write clean, clear code examples and tutorials in Python / JavaScript\n• Passion for community building and public speaking",
                "benefits": "• Global travel budget for conferences\n• High autonomy and flexible remote schedule\n• Full healthcare package",
                "deadline": datetime.utcnow() + timedelta(days=35)
            }
        ]

        for jdata in jobs_data:
            job = Job(
                employer_id=jdata["employer"].id,
                category_id=jdata["category"].id,
                title=jdata["title"],
                job_type=jdata["job_type"],
                experience_level=jdata["experience_level"],
                location=jdata["location"],
                is_remote=jdata["is_remote"],
                salary_currency=jdata["salary_currency"],
                salary_min=jdata["salary_min"],
                salary_max=jdata["salary_max"],
                skills_required=jdata["skills_required"],
                description=jdata["description"],
                requirements=jdata["requirements"],
                benefits=jdata["benefits"],
                deadline=jdata["deadline"],
                status="active"
            )
            db.session.add(job)

        db.session.commit()

        print("4. Seeding Job Seeker Accounts & Profiles...")
        
        # Candidate 1: Alex Rivera
        seeker1 = User(username="alex_rivera", email="candidate@example.com", role="jobseeker")
        seeker1.set_password("password123")
        db.session.add(seeker1)
        db.session.flush()

        p1 = UserProfile(
            user_id=seeker1.id,
            full_name="Alex Rivera",
            headline="Senior Full-Stack Engineer | Python, React & Cloud Architecture",
            phone="+1 (555) 234-5678",
            location="San Francisco, CA",
            experience_years=6,
            education="B.S. in Computer Science - UC Berkeley",
            skills="Python, Flask, React, TypeScript, PostgreSQL, Docker, AWS, Redis",
            bio="Passionate software engineer with 6+ years of experience building high-throughput web applications and scalable microservices. Enthusiast for clean architecture, automated testing, and developer tooling.",
            resume_filename="sample_alex_rivera_resume.pdf",
            linkedin_url="https://linkedin.com/in/alexrivera-dev",
            github_url="https://github.com/alexrivera-dev",
            portfolio_url="https://alexrivera.dev"
        )
        db.session.add(p1)

        # Candidate 2: Sarah Chen
        seeker2 = User(username="sarah_chen", email="sarah.chen@example.com", role="jobseeker")
        seeker2.set_password("password123")
        db.session.add(seeker2)
        db.session.flush()

        p2 = UserProfile(
            user_id=seeker2.id,
            full_name="Sarah Chen",
            headline="Lead UI/UX Designer & Design Systems Architect",
            phone="+1 (555) 876-5432",
            location="Austin, TX",
            experience_years=7,
            education="B.A. in Interaction Design - RISD",
            skills="Figma, UI/UX Design, Design Systems, Wireframing, User Testing, HTML/CSS",
            bio="Lead designer passionate about simplifying complex workflows into elegant, human-centered digital experiences.",
            resume_filename="sample_sarah_chen_resume.pdf",
            linkedin_url="https://linkedin.com/in/sarahchen-design",
            portfolio_url="https://sarahchen.design"
        )
        db.session.add(p2)

        db.session.commit()

        print("5. Seeding Sample Applications & Saved Jobs...")
        first_job = Job.query.filter_by(title="Senior Full-Stack Python Engineer").first()
        second_job = Job.query.filter_by(title="Lead UI/UX Product Designer").first()
        third_job = Job.query.filter_by(title="Machine Learning Research Engineer").first()

        if first_job:
            app1 = Application(
                job_id=first_job.id,
                seeker_id=seeker1.id,
                cover_note="I am thrilled to apply for the Senior Full-Stack Python Engineer position at TechCorp Global. With over 6 years of experience building scalable Flask microservices and React frontends, I am confident I can make an immediate impact on your transaction systems.",
                resume_filename="sample_alex_rivera_resume.pdf",
                status="Shortlisted"
            )
            db.session.add(app1)

        if second_job:
            app2 = Application(
                job_id=second_job.id,
                seeker_id=seeker2.id,
                cover_note="Hello Nexus team! I have built and scaled multi-brand design systems for hyper-growth tech companies and would love to lead design projects at your studio.",
                resume_filename="sample_sarah_chen_resume.pdf",
                status="Reviewed"
            )
            db.session.add(app2)

        if third_job:
            save1 = SavedJob(seeker_id=seeker1.id, job_id=third_job.id)
            db.session.add(save1)

        db.session.commit()
        print("\n=== SUCCESS: Database seeded successfully with demo accounts! ===")
        print("Demo Accounts:")
        print("Candidate:  email: candidate@example.com    password: password123")
        print("Employer:   email: recruiter@techcorp.com   password: password123")
        print("Employer 2: email: careers@innovatelabs.io  password: password123")

if __name__ == '__main__':
    seed_database()
