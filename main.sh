echo "Select on of the following actions to execute:"
echo "  1) Scrape (WARNING: it may take some time)"
echo "  2) Index (WARNING: it may take some time)"
echo "  3) Benchmark"
echo "  4) Search"
echo "  5) Run Flask App (try the search engine on a web server)"

printf "Type one of the actions (1-5) or anything else to exit, then press Enter: "

read ans

case $ans in

    '1')
    python3 scrape.py
    ;;

    '2')
    python3 index.py
    ;;

    '3')
    python3 execute_benchmark.py
    ;;

    '4')
    echo 'Type your query:'
    read query
    python3 search.py "$query"
    ;;

    '5')
    flask --app flask_app.py run
    ;;

    *)
    exit 0
    ;;
esac