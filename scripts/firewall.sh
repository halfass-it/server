sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow from 127.0.0.1 to any port 6000
sudo ufw allow from 127.0.0.1 to any port 7000
sudo ufw allow from 127.0.0.1 to any port 6001
sudo ufw allow from 127.0.0.1 to any port 6002
sudo ufw allow from 127.0.0.1 to any port 7001
sudo ufw allow from 127.0.0.1 to any port 7002
sudo ufw allow from 127.0.0.1 to any port 1337
sudo ufw allow from 127.0.0.1 to any port 1338
sudo ufw allow from 127.0.0.1 to any port 1339
sudo ufw allow from 127.0.0.1 to any port 1340
sudo ufw deny 6000/tcp
sudo ufw deny 7000/tcp
sudo ufw deny 6001/tcp
sudo ufw deny 6002/tcp
sudo ufw deny 7001/tcp
sudo ufw deny 7002/tcp
sudo ufw deny 1337/tcp
sudo ufw deny 1338/tcp
sudo ufw deny 1339/tcp
sudo ufw deny 1340/tcp

