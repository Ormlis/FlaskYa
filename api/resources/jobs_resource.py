from datetime import datetime

from flask import jsonify
from flask_restful import abort, Resource

from api.resources.parser_job import *
from data import *


def abort_if_job_not_found(job_id):
    session = create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify(
            {
                'job': job.to_dict(only=('id',
                                         'team_leader', 'job', 'work_size', 'collaborators',
                                         'start_date', 'end_date',
                                         'is_finished'))
            }
        )

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, job_id):
        abort_if_job_not_found(job_id)
        args = put_parser.parse_args()
        session = create_session()
        job = session.query(Jobs).get(job_id)
        job.team_leader = args.get('team_leader', job.team_leader)
        job.job = args.get('job', job.job)
        job.work_size = args.get('work_size', job.work_size)
        job.collaborators = args.get('collaborators', job.collaborators)
        job.start_date = datetime.fromisoformat(
            args.get('start_date', job.start_date.isoformat()))
        job.end_date = datetime.fromisoformat(
            args.get('end_date', job.end_date.isoformat()))
        job.is_finished = args.get('is_finished', job.is_finished)
        session.merge(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(only=('id',
                                                    'team_leader', 'job', 'work_size',
                                                    'collaborators',
                                                    'start_date', 'end_date',
                                                    'is_finished')) for item in jobs]})

    def post(self):
        args = post_parser.parse_args()
        session = create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            start_date=datetime.fromisoformat(args['start_date']),
            end_date=datetime.fromisoformat(args['end_date']),
            is_finished=args['is_finished'],
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})
