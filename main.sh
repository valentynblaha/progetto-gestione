echo "Select on of the following actions to execute:"
echo "  1) Scrape (WARNING: may take some time)"
echo "  2) Index (WARNING: may take some time)"
echo "  3) Benchmark"
echo "  4) Search"
echo "  5) Run Flask App (try the search engine on a server)"

printf "Type one of the actions (1-5) or anything else to exit, then press Enter: "

read ans

case $ans in

    '1')
    echo 'Scrape'
    ;;

    '2')
    echo 'Index'
    ;;

    '3')
    echo 'Benchmark'
    ;;

    '3')
    echo 'Seacrh'
    ;;

    '3')
    echo 'Flask'
    ;;

    *)
    exit
    ;;
esac