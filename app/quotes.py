from datetime import date

_quotes = [
    {
        "text": "A cada dia uma nova chance para recomeçar. Aproveite cada atendimento como uma oportunidade de transformar o dia de alguém.",
        "author": "Chico Xavier"
    },
    {
        "text": "O bem que você faz hoje é a semente que floresce amanhã. Plante com carinho cada gesto.",
        "author": "André Luiz"
    },
    {
        "text": "A paciência é a arte de cultivar a esperança. No silêncio do servir, encontramos a paz.",
        "author": "Emmanuel"
    },
    {
        "text": "Fora da caridade não há salvação. E a caridade começa com um sorriso, uma escuta, um gesto de amor ao próximo.",
        "author": "Allan Kardec"
    },
    {
        "text": "Nascer, morrer, renascer ainda e progredir sempre, tal é a lei. Cada desafio é um degrau na sua evolução.",
        "author": "Allan Kardec"
    },
    {
        "text": "A verdadeira caridade é ser benevolente para com todos, indulgente para com as imperfeições alheias e perdoar as ofensas.",
        "author": "Allan Kardec"
    },
    {
        "text": "Não existe encontro por acaso. Cada cliente que chega até você traz uma história e uma lição.",
        "author": "Bezerra de Menezes"
    },
    {
        "text": "O trabalho é a chave do progresso. Cada piercing colocado, cada atendimento realizado, é um passo adiante.",
        "author": "Meimei"
    },
    {
        "text": "Agradecer é reconhecer que a vida é feita de dádivas. Comece o dia com gratidão no coração.",
        "author": "Irmão José"
    },
    {
        "text": "A evolução começa quando a gente se permite aprender. Cada erro é um professor, cada acerto um incentivo.",
        "author": "Joanna de Ângelis"
    },
    {
        "text": "O sucesso é a soma de pequenos esforços repetidos dia após dia. Persista com fé e determinação.",
        "author": "Roberto Shinyashiki"
    },
    {
        "text": "Seja a razão pela qual alguém sorri hoje. A gentileza é a luz que ilumina o caminho de todos.",
        "author": "Desconhecido"
    },
    {
        "text": "A vida é feita de pequenos gestos que constroem grandes histórias. Cada atendimento é um capítulo.",
        "author": "Desconhecido"
    },
    {
        "text": "O propósito da vida é a evolução. E evoluímos através do serviço ao próximo, com amor e dedicação.",
        "author": "Léon Denis"
    },
    {
        "text": "A fé sem obras é morta. Que seu trabalho seja sua melhor oração.",
        "author": "Cairbar Schutel"
    },
    {
        "text": "Perdoar é libertar-se. Não carregue mágoas — cada novo dia é uma página em branco.",
        "author": "Divaldo Franco"
    },
    {
        "text": "A felicidade não está no ter, mas no ser. E ser feliz é fazer feliz.",
        "author": "Amélia Rodrigues"
    },
    {
        "text": "O amor ao próximo é a maior terapia. Cure sorrindo, atenda com alma, viva com propósito.",
        "author": "Hammed"
    },
    {
        "text": "Plante pensamentos bons, colha ações nobres. Sua mente é o jardim da sua vida.",
        "author": "Buda"
    },
    {
        "text": "A calma é a fortaleza dos fortes. Em meio ao caos, respire, confie e siga.",
        "author": "Confúcio"
    },
    {
        "text": "O que você faz hoje pode melhorar o amanhã de alguém. Nunca subestime o poder de um gesto de bondade.",
        "author": "Madre Teresa de Calcutá"
    },
    {
        "text": "A simplicidade é o mais alto grau de sofisticação. Atenda com simplicidade, mas com excelência.",
        "author": "Leonardo da Vinci"
    },
    {
        "text": "Não espere por grandes oportunidades. Crie-as com pequenas atitudes diárias.",
        "author": "Napoleon Hill"
    },
    {
        "text": "O conhecimento fala, mas a sabedoria escuta. Ouça seus clientes, aprenda com eles.",
        "author": "Jimmy Hendrix"
    },
    {
        "text": "A arte de viver está em saber equilibrar o fazer e o ser. Trabalhe com propósito, viva com leveza.",
        "author": "Epiteto"
    },
    {
        "text": "Sua energia atrai sua realidade. Cultive pensamentos positivos e veja o universo conspirar a seu favor.",
        "author": "Desconhecido"
    },
    {
        "text": "O impossível é só questão de opinião. Acredite no seu potencial e vá além.",
        "author": "Augusto Cury"
    },
    {
        "text": "A arte de ser feliz está em saber valorizar o que se tem. Hoje é um presente — viva cada segundo.",
        "author": "Desconhecido"
    },
    {
        "text": "Transforme cada desafio em aprendizado, cada queda em impulso, cada dia em uma nova chance.",
        "author": "Paulo Coelho"
    },
    {
        "text": "Ninguém cruza nosso caminho por acaso. Cada cliente é um mestre disfarçado. Aprenda a lição.",
        "author": "Desconhecido"
    },
]

def quote_of_the_day():
    hoje = date.today()
    dia_do_ano = hoje.timetuple().tm_yday
    idx = (dia_do_ano - 1) % len(_quotes)
    return _quotes[idx]
