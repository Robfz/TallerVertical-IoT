import time
import User

from firebase import firebase

database = firebase.FirebaseApplication('https://spot2016.firebaseio.com', None)


def dispatch_job(job):
    user_name = job['user']
    user_json = database.get('/usuarios/' + user_name, None)
    user = User.User(user_json['email'], user_json['horario']['Monday'],
                     user_json['name'], user_json['placas'])
    return user


def main():
    while 1:
        jobs = database.get('/jobs', None)
        for job in jobs:
            dispatch_job(job)
        time.sleep(1.0)


if __name__ == '__main__':
    main()
