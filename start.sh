# check that docker compose file exists
if [ ! -f docker-compose.yml ]; then
    echo "docker-compose.yml not found"
    exit 1
fi

# create or check that models folder exists
if [ ! -d model ]; then
    mkdir model
fi



# down model from https://huggingface.co/IlyaGusev/saiga2_13b_gguf/blob/main/model-q5_K.gguf using curl
if [ ! -f model/model-q5_K.gguf ]; then
    curl https://disk.yandex.ru/d/WYWiilWabEnXnQ --output model/model-q5_K.gguf
fi

cp config/.env.template config/.env


cp config/.env.template config/.env
docker compose up -d
