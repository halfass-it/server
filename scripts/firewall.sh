sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow from 127.0.0.1 to any port 5000
sudo ufw allow from 127.0.0.1 to any port 6000
sudo ufw allow from 127.0.0.1 to any port 7000
sudo ufw allow from 127.0.0.1 to any port 6001
sudo ufw allow from 127.0.0.1 to any port 6002
sudo ufw allow from 127.0.0.1 to any port 7001
sudo ufw allow from 127.0.0.1 to any port 7002
sudo ufw allow from 127.0.0.1 to any port 5001
sudo ufw allow from 127.0.0.1 to any port 5002
sudo ufw allow from 127.0.0.1 to any port 5003
sudo ufw allow from 127.0.0.1 to any port 5004
sudo ufw deny 5000/tcp
sudo ufw deny 6000/tcp
sudo ufw deny 7000/tcp
sudo ufw deny 5001/tcp
sudo ufw deny 5002/tcp
sudo ufw deny 5003/tcp
sudo ufw deny 5004/tcp
sudo ufw deny 6001/tcp
sudo ufw deny 6002/tcp
sudo ufw deny 7001/tcp
sudo ufw deny 7002/tcp