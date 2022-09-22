clear
echo "Ajuda com a linha de comando"
echo "python -m receitaws --help"
python -m receitaws --help
sleep 5
echo "CPF no arquivo cpf.csv, chamada somente os parâmetros obrigatórios"
echo 'python -m receitaws "cpf.csv" 31888916877 --origem "Teste DS"'
echo 'Valores padrão: salvo em resultados.csv, com consulta em Desenvolvimento e com cache de 36 meses'
echo ''
sleep 3
echo "Mudando o ambiente para Sustentação"
echo 'python -m receitaws "cpf.csv" 31888916877 --ambiente su --origem "Teste SU"'
sleep 3
echo ''
echo "Mudando o ambiente para Homologação"
echo 'python -m receitaws "dados\cpf.csv" 31888916877 --ambiente hm --origem "Teste HM"'
echo ''
sleep 3
echo "Mudando o ambiente para Produção"
echo 'python -m receitaws "cpf.csv" 31888916877 --ambiente pd --origem "Teste PD"'
echo ''
sleep 3

