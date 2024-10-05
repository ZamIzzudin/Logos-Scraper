import os
from server import create_app, start_scheduler, stop_scheduler


app = create_app()
start_scheduler(5) # Time interval (in hours) -> scheduler called every 5 hours

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 8080))  
        app.run(host="0.0.0.0",port=port)
    except (KeyboardInterrupt, SystemExit):
        stop_scheduler()