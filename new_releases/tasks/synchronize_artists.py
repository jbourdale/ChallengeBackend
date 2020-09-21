from celery import shared_task


@shared_task
def synchronize_artists():
    print("SYNCHRONIZE ARTISTS TASK")


