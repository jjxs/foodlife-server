# Install
### install docker
    sudo apt update -y
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt update -y
    sudo apt -y install docker-ce docker-ce-cli containerd.io
    sudo gpasswd -a ubuntu docker
### install docker-compose
    sudo apt-get install docker-compose-plugin
    sudo apt-get install docker-compose
### install awscli
    sudo apt-get install awscli



## login awscli
    sudo apt install gnupg2 pass


#### config
    aws configure

    region = ap-northeast-1
    aws_access_key_id = AKIAZS4IIOPMBLSPYGDJ
    aws_secret_access_key = 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

    
    aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 659026375640.dkr.ecr.ap-northeast-1.amazonaws.com


## Install Nginx
    sudo apt install -y nginx



## Docker Image
#### Build
    cd foodlife-client/docker
    docker build -t foodlife-client:1.9.2 .

#### Tag
    docker tag foodlife-client:1.9.2 659026375640.dkr.ecr.ap-northeast-1.amazonaws.com/foodlife-client:1.9.2

#### Push
    docker push 659026375640.dkr.ecr.ap-northeast-1.amazonaws.com/foodlife-client:1.9.2




#### Start docker Image
    cd client
    vi docker-compose.yml #  修改对应版本信息

    docker-compose up -d

