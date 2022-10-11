from TownIssues import create_app

class DebugConfig:
    SECRET_KEY = 'b76d4859dd2d340dfe47dbf8993f0386'
    SQLALCHEMY_DATABASE_URI = 'postgresql://xrazzggtkegawp:38c7259d2fb0f773960265fa484c1725954e22d58496cc988aa6697a8c4f6b6a@ec2-54-194-180-51.eu-west-1.compute.amazonaws.com:5432/dfur7dcgfmutjb'

app = create_app(DebugConfig)

if __name__ == '__main__':
    app.run(debug=True)
