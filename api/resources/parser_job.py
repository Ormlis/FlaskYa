from flask_restful import reqparse

post_parser = reqparse.RequestParser()
post_parser.add_argument('team_leader', required=True, type=int)
post_parser.add_argument('job', required=True)
post_parser.add_argument('work_size', required=True, type=int)
post_parser.add_argument('collaborators', required=True)
post_parser.add_argument('start_date', required=True)
post_parser.add_argument('end_date', required=True)
post_parser.add_argument('is_finished', required=True, type=bool)

put_parser = reqparse.RequestParser()
post_parser.add_argument('team_leader', type=int)
post_parser.add_argument('job')
post_parser.add_argument('work_size', type=int)
post_parser.add_argument('collaborators')
post_parser.add_argument('start_date')
post_parser.add_argument('end_date')
post_parser.add_argument('is_finished', type=bool)
