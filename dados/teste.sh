echo "Ajuda com a linha de comando"
echo "python -m receitaws --help"
python -m receitaws --help
sleep 5
echo "CPF no arquivo cpf.csv, chamada somente os parâmetros obrigatórios"
echo 'python -m receitaws "cpf.csv" 31888916877 --origem "Teste DS"'
python -m receitaws 'cpf.csv' 31888916877 --origem "Teste DS"
echo 'Valores padrão: salvo em resultados.csv, com consulta em Desenvolvimento e com cache de 36 meses'
sleep 3
clear
echo "Mudando o ambiente para Sustentação"
echo 'python -m receitaws "cpf.csv" 31888916877 --ambiente su --origem "Teste SU"'
python -m receitaws --help
python -m receitaws "cpf.csv" 31888916877 --ambiente su --origem "Teste SU"
sleep 3
clear
echo "Mudando o ambiente para Homologação"
python -m receitaws --help
echo 'python -m receitaws "dados\cpf.csv" 31888916877 --ambiente hm --origem "Teste HM"'
python -m receitaws "cpf.csv" 31888916877 --ambiente hm --origem "Teste HM"
sleep 3
clear
echo "Mudando o ambiente para Produção"
echo 'python -m receitaws "cpf.csv" 31888916877 --ambiente pd --origem "Teste PD"'
python -m receitaws "cpf.csv" 31888916877 --ambiente pd --origem "Teste PD"
sleep 3
clear


