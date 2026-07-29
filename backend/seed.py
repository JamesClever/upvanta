from app import create_app
from app.extensions import db
from app.models.job import Job

app = create_app()

with app.app_context():

    if Job.query.count() == 0:

        sample_jobs = [

            Job(
                title="Python Backend Developer",
                company="Microsoft",
                location="Remote",
                job_type="Full-time",
                category="Software Development",
                salary="$90,000/year",
                description="Develop backend APIs using Python and Flask."
            ),

            Job(
                title="Frontend Web Developer",
                company="Google",
                location="Remote",
                job_type="Full-time",
                category="Web Development",
                salary="$85,000/year",
                description="Build responsive user interfaces using HTML, CSS and JavaScript."
            ),

            Job(
                title="AI Prompt Engineer",
                company="OpenAI",
                location="Remote",
                job_type="Contract",
                category="Artificial Intelligence",
                salary="$100,000/year",
                description="Design prompts and AI workflows for business applications."
            )

        ]

        db.session.add_all(sample_jobs)
        db.session.commit()

        print("✅ Sample jobs added successfully!")

    else:
        print("ℹ️ Jobs already exist.")