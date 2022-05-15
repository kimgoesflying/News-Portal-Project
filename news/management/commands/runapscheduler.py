import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.contrib.auth.models import User
from news.models import Post, Subscriber
from datetime import datetime, timedelta

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


def news_weekly_mail():
    one_week_ago = datetime.today() - timedelta(days=7)
    new_posts = Post.objects.filter(date__gte=one_week_ago)
    subscribers = Subscriber.objects.all()

    for sub in subscribers:
        username = User.objects.get(email=sub)
        mail_posts = new_posts.filter(category__subscriber__mail=sub)

        html_content = render_to_string(
            'news/mail_news_post_list.html',
            {
                'mail_posts': mail_posts,
                'username': username,
            }
        )

        msg = EmailMultiAlternatives(
            subject='NewsPortal weekly',
            to=[sub],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print('--------', 'mail sent to', sub)


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            news_weekly_mail,
            trigger=CronTrigger(day_of_week="mon"),
            id="news_weekly_mail",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'news_weekly_mail'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
