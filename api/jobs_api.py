from datetime import datetime

import flask
from flask import jsonify, request

from data import *

blueprint = flask.Blueprint('jobs_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id',
                                    'team_leader', 'job', 'work_size', 'collaborators',
                                    'start_date', 'end_date',
                                    'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    session = create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('id',
                                       'team_leader', 'job', 'work_size', 'collaborators',
                                       'start_date', 'end_date',
                                       'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators',
                  'start_date', 'end_date',
                  'is_finished']):
        return jsonify({'error': 'Bad request'})
    session = create_session()
    if session.query(Jobs).get(request.json['id']):
        return jsonify({'error': 'Id already exists'})
    jobs = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=datetime.fromisoformat(request.json['start_date']),
        end_date=datetime.fromisoformat(request.json['end_date']),
        is_finished=request.json['is_finished'],
    )
    session.add(jobs)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    session = create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    session.delete(jobs)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def edit_jobs(jobs_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    session = create_session()
    job = session.query(Jobs).get(jobs_id)
    if not job:
        return jsonify({'error': 'Not found'})
    job.team_leader = request.json.get('team_leader', job.team_leader)
    job.job = request.json.get('job', job.job)
    job.work_size = request.json.get('work_size', job.work_size)
    job.collaborators = request.json.get('collaborators', job.collaborators)
    job.start_date = datetime.fromisoformat(
        request.json.get('start_date', job.start_date.isoformat()))
    job.end_date = datetime.fromisoformat(request.json.get('end_date', job.end_date.isoformat()))
    job.is_finished = request.json.get('is_finished', job.is_finished)
    session.merge(job)
    session.commit()
    return jsonify({'success': 'OK'})
