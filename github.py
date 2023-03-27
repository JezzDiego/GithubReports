import requests
import datetime

def get_pull_requests(pulls_num):
    try:
        response = requests.get("https://api.github.com/repos/dadosjusbr/site/pulls?state=closed&per_page=" + str(pulls_num))
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code
    except Exception as e:
        print("---> Verifique sua conexão com a internet! <---\n", e)

def generate_report(pulls):
    try:
        now = datetime.datetime.now()
        date = now.strftime("%d-%m-%Y")
        hour = now.strftime("%H:%M:%S")
        file_name = "report_" + date + "_" + hour + ".txt"
        file = open(file_name, "w")
        file.write("Relatório de Pull Requests fechados no dia " + date + " às " + hour + ":\n")
        for pr in pulls:
            closing_date = pr['closed_at'].split('T')[0].split('-')
            file.write("\n-> " + pr['title'] + "\n")
            file.write("Autor: " + pr['user']['login'] + "\n")
            file.write("Descrição: \n" + pr['body'] + "\n\n")
            file.write("Data de fechamento: " + "{}/{}/{}".format(closing_date[2], closing_date[1], closing_date[0]) + "\n")
            file.write("Link: " + pr['html_url'] + "\n")
        file.close()
        print("\nRelatório gerado com sucesso!\n")
    except Exception as e:
        print("---> Erro ao gerar relatório! <---\n", e)

print("\n10 últimos Pull Requests fechados:\n")
for pr in get_pull_requests(10):
    print("-> " + pr['title'])

num = int(input("\nDigite o número de pull requests que deseja selecionar: "))
pulls = get_pull_requests(num)

generate_report(pulls)
