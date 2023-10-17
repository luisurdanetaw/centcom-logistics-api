from model.tmr import Tmr
import repository.dummy_db as tmr_repository

async def create_tmr(tmr: Tmr):
    if tmr.weight >= 0 and tmr.containers >= 0:
        try: 
            return await tmr_repository.create_tmr(tmr)
        except Exception as e:
            print(f"Error creating tmr ticket {e}")
        
    else:
        return print("no good")

