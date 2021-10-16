import csv
import sys
import psycopg2
from unidecode import unidecode
from datetime import datetime
import re

conn = psycopg2.connect(database='postgres', user='postgres',
                        password='123456', host='localhost', port='5432')
tiposVeiculos, tiposInfrator, tiposGravidade, tiposInfracao = [], [], [], []
cur = conn.cursor()


def trataVeiculo(row):
    nome = unidecode(row[3].strip().upper())
    if nome not in tiposVeiculos:
        tiposVeiculos.append(nome)
        cur.execute("""INSERT INTO "tarefa-ceub"."tipo-veiculo" ("codigo-veiculo", "nome-veiculo")
            values (%s, %s) RETURNING "codigo-veiculo"; """, (len(tiposVeiculos), nome,))
        return cur.fetchone()
    return tiposVeiculos.index(nome) + 1


def trataGravidade(row):
    nome = unidecode(row[-1].strip().upper())
    if nome not in tiposGravidade:
        tiposGravidade.append(nome)
        cur.execute("""INSERT INTO "tarefa-ceub"."tipo-gravidade" ("codigo-gravidade", "nome-gravidade")
            VALUES (%s, %s) RETURNING "codigo-gravidade"; """, (len(tiposGravidade), nome,))
        return cur.fetchone()
    return tiposGravidade.index(nome) + 1


def trataInfrator(row):
    nome = unidecode(row[2].strip().upper())
    if nome not in tiposInfrator:
        tiposInfrator.append(nome)
        cur.execute("""INSERT INTO "tarefa-ceub"."tipo-infrator" ("codigo-infrator", "nome-infrator")
            VALUES (%s, %s) RETURNING "codigo-infrator"; """, (len(tiposInfrator), nome,))
        return cur.fetchone()
    return tiposInfrator.index(nome) + 1


def trataInfracao(row):
    id = row[0].replace("-", "")
    if id not in tiposInfracao:
        tiposInfracao.append(id)
        nome = unidecode(row[1].strip().lower())
        cur.execute("""INSERT INTO "tarefa-ceub"."tipo-infracao" ("codigo-tipo-infracao", "nome-tipo-infracao")
            values (%s, %s) RETURNING "codigo-tipo-infracao"; """, (id, nome,))
        return cur.fetchone()
    return id


def main():
    print("teste")
    with open('dados-abertos-julho.csv', "r", newline='', encoding='utf-8') as lista:
        csv_data = csv.reader(lista, delimiter=';')
        # print(csv_data)
        header = next(csv_data)
        print(header)
        primeira = next(csv_data)
        exit
        i = 0
        for row in csv_data:
            tipoInfracao = trataInfracao(row)
            tipoInfrator = trataInfrator(row)
            tipoVeiculo = trataVeiculo(row)
            tipoGravidade = trataGravidade(row)

            data = row[4].strip()
            hora = row[5].strip()
            dataEHora = data + ' ' + hora
            objDataEHora = datetime.strptime(dataEHora, '%d/%m/%Y %H:%M')
            # print(dataEHora)
            # print(objDataEHora)

            rodovia = row[6]
            kilometro = row[7]
            complemento = row[8]
            # print("+++++ RODOVIA -------", rodovia)
            if kilometro == "":
                endereco = rodovia
                posicaoKM = rodovia.find("KM")
                rodovia = endereco[0:posicaoKM].strip()
                # print(rodovia)
                regexEnd = re.search("KM\s?([\d,.]+)", endereco)
                # print(regexEnd)
                if(regexEnd):
                    kilometro = regexEnd.group()
                    # print(kilometro)
                if kilometro != '':
                    complemento = endereco[endereco.find(
                        kilometro)+len(kilometro)::].strip()
                # print(complemento)

            # if (row[-2], row[-3]) == ("",""):
            #     print('latitude e longitude vazios')
            # else:
            #     print('+++++ achou um prrenchido', row[-2], row[-3])
            #     print(row[-3].strip().isalnum())

            try:
                latitude = float(row[-3].strip())
                longitude = float(row[-2].strip())
            except ValueError:
                latitude = 0
                longitude = 0
            # print("+++", row[-3], latitude)

            cur.execute(""" INSERT INTO "tarefa-ceub".infracao
                ("codigo-infracao", "codigo-tipo-infracao", "codigo-tipo-veiculo", "codigo-tipo-infrator", "codigo-tipo-gravidade",
                "horario-infracao", rodovia, "km-rodovia", "local-complemento", "local-longitude", "local-latitude")
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s);
                """, (i, tipoInfracao, tipoVeiculo, tipoInfrator, tipoGravidade, objDataEHora, rodovia, kilometro, complemento, latitude, longitude))

            # print(row[3])
            i += 1
            # if i == 150:
            #     break

    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
