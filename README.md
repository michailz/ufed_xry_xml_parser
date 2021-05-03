# ufed_xry_xml_parser
1. install docker + docker-compose
2. from the docker_files directory run:
    docker-compose up -d
3. connect to adminer localhost:8080
   System:Postgresql
   Server:pgs
   User:postgres
   password:root
   
4. Import phonebook.sql
5. Create file directory in root (directory where main.py is)
6. Put ufed and xry xml into file directory
7. Make sure you have up to 12 GB RAM and python can use it 
   (BeautifulSoup with large XMLS sucks)