from utils import db

class NPCQuery():
    conn, cursor = None, None
    
    table_name = 'npc_agents'
    
    def __init__(self):
        self.conn = db.conn
        self.cursor = self.conn.cursor()
        self.create_table_if_not_exist()
        

    def create_table_if_not_exist(self):            
        query = f'''CREATE TABLE IF NOT EXISTS {self.table_name}(  
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                profile_url VARCHAR UNIQUE,
                name VARCHAR NULL,
                email VARCHAR UNIQUE NULL,
                address TEXT NULL,
                phone VARCHAR NULL,
                whatsapp VARCHAR NULL
            );'''
        self.cursor.execute(query)
        self.conn.commit()
        
            
    def insert_profile_url(self, profile_url: str):
        self.cursor.execute(f"INSERT INTO {self.table_name}(profile_url) VALUES(?)", (profile_url,))
        self.conn.commit()
        
    
    def get_total(self, only_with_email):
        where_clause = 'WHERE email IS NOT NULL' if only_with_email else ''
        query = f"SELECT count(*) FROM {self.table_name} {where_clause}"
        return self.cursor.execute(query).fetchone()[0]
        

    def get_npc_agents(self, progress_idx=0, only_with_email=False):
        # Build base query with optional WHERE clause
        where_clause = "WHERE email IS NOT NULL" if only_with_email else ""
        query = f"SELECT * FROM {self.table_name} {where_clause} LIMIT -1 OFFSET {progress_idx}"

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Map rows to dictionaries
        result = [
            {
                'id': row[0],
                'profile_url': row[1],
                'name': row[2],
                'email': row[3],
                'address': row[4],
                'phone': row[5],
                'whatsapp': row[6],
            }
            for row in rows
        ]

        return result

    
    
    def update_agent(self, agent_id: int, data: dict):
        query = f''' 
            UPDATE {self.table_name} 
            SET 
                name = ?, 
                email = ?,
                address = ?, 
                phone = ?, 
                whatsapp = ?
            WHERE
                id = ?
        '''
        try:
                
            self.cursor.execute(query, (
                data.get('name'), 
                data.get('email'), 
                data.get('address'), 
                data.get('phone'), 
                data.get('whatsapp'),
                agent_id,
                )
            )
            self.conn.commit()
        except Exception as e: 
            print('Error Caught:', e)
            