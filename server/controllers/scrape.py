from ..utils import Utils
from ..config.db import db_connection

def scrape_store_data():
    utils = Utils()
    # DB Initialize
    db = db_connection('scrapes') 

    # Start Scraping Function
    data = utils.scrape_data()
    new_data = []

    # Change Status To Unvisible For All Anchor Data
    db.update_many({},{'$set':{'is_show':False}})

    for item in data:
        if not db.find_one({'kode_tender': item['kode_tender']}):
            new_data.append(item)
        else:
            # Change Status To Visible For Active Data
            db.update_one({'kode_tender': item['kode_tender']},{"$set":{'is_show':True}})

    if new_data:
        # Add New Data 
        db.insert_many(new_data)
        
    response = {
        'status': 'success',
        'message': 'Success Scrape and Store Data',
        'data_found': len(data),
        'new_data': len(new_data),
    }
    
    return response