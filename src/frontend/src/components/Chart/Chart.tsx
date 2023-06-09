import React, {useEffect, useState} from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import Select, { components } from "react-select";
import './Chart.css';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

export const initialOptions = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top',
        },
        title: {
            display: true,
            text: 'График',
        },
    },
};

const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];

export const initialData = {
    labels,
    datasets: [
        {
            label: 'Dataset 1',
            data: [1, 3, 2, 4, 7, 6, 5, 8],
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
        },
        {
            label: 'Dataset 2',
            data: [1, 2, 6, 8, 5, 7, 4, 3],
            borderColor: 'rgb(53, 162, 235)',
            backgroundColor: 'rgba(53, 162, 235, 0.5)',
        },
    ],
};

const durationOptions = [
    { label: 'Краткосрочно', value: 'Краткосрочно' },
    { label: 'Среднесрочно', value: 'Среднесрочно' },
    { label: 'Долгосрочно', value: 'Долгосрочно' },
]

const Chart = () => {
    const [input, setInput] = useState("");
    const [product, setProduct] = useState("18AA2603B271C19A581133BD34319311");
    const [duration, setDuration] = useState();
    const [dates, setDates] = useState([]);
    const [firstPrices, setFirstPrices] = useState([]);
    const [secondPrices, setSecondPrices] = useState([]);
    const [demands, setDemands] = useState([]);
    const [profits, setProfits] = useState([]);
    const [data, setData] = useState(initialData);
    const [options, setOptions] = useState([]);
    const [chartOptions, setChartOptions] = useState();
    const [isDemandForecast, setDemandForecast] = useState(false);
    const [isOptimalPrice, setOptimalPrice] = useState(false);
    const [bestPrice, setBestPrice] = useState(0);

    useEffect(() => {
      fetch("http://84.201.153.183:8000/categories", {
          headers: {
              'Access-Control-Allow-Origin': '*'
          }
      })
        .then(response => {
          return response.json()
        })
        .then(data => {
          console.log(data);
          setOptions(data.categories);
        });
    }, []);

    useEffect(() => {
        const value = options.map((option) => {
            return {
                label: option,
                value: option,
            };
        });
        setChartOptions(value);
    }, [options]);

    const handleDemandClick = () => {
        console.log(product);
        console.log(duration);
        fetch('http://84.201.153.183:8000/')
          .then((res) => console.log(res));
        fetch('http://84.201.153.183:8000/predict/demand', {
            method: "POST",
            mode: 'cors',
            headers: {
                "Content-Type": "application/json",
                'Access-Control-Allow-Origin': '*',
            },
            body: JSON.stringify({
                name_product: product,
                type_predict: duration,
                id_market: "6B8E111AB5B5C556C0AEA292ACA4D88B"
            })
        })
            .then(function(response) {
                return response.json();
            })
            .then(function(response) {
                console.log(response);
                setDates(response.dates);
                setDemands(response.demands);
            });
        setDemandForecast(true);
        setOptimalPrice(false);
    };

    const handleOptimalPriceClick = () => {
        fetch('http://84.201.153.183:8000/predict/price', {
            method: "POST",
            mode: 'cors',
            headers: {
                "Content-Type": "application/json",
                'Access-Control-Allow-Origin': '*',
            },
            body: JSON.stringify({
                name_product: product,
                type_predict: duration,
                id_market: "6B8E111AB5B5C556C0AEA292ACA4D88B"
            })
        })
            .then(function(response) {
                return response.json();
            })
            .then(function(response) {
                setFirstPrices(response.demand.prices);
                setDemands(response.demand.demands);
                setSecondPrices(response.profit.prices);
                setProfits(response.profit.profits);
                setBestPrice(response.best_price);
            });
        setOptimalPrice(true);
        setDemandForecast(false);
    }

    const render = () => {
        if (isDemandForecast) {
            const data = {
                labels: dates,
                datasets: [
                    {
                        label: 'Спрос',
                        data: demands,
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    },
                ],
            };
            return <Line options={initialOptions} data={data}/>
        } else if (isOptimalPrice) {
            const data1 = {
                labels: firstPrices,
                datasets: [
                    {
                        label: 'Спрос',
                        data: demands,
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    },
                ],
            };
            const data2 = {
                labels: secondPrices,
                datasets: [
                    {
                        label: 'Оборот',
                        data: profits,
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    },
                ],
            };
            return <>
                <div className='price'>
                    <h2 className='price__title title'>Лучшая цена:</h2>
                    <div className='best-price'>{bestPrice}</div>
                </div>
                <Line options={initialOptions} data={data1}/>
                <Line options={initialOptions} data={data2}/>
            </>
        }
    }

    return (
        <>
          <div className='select-area'>
              <h2 className='title'>Выберите продукт</h2>
              <Select
                options={chartOptions}
                autoFocus={true}
                className='select'
                onChange={(product) => setProduct(product.value)}
              />
              <Select
                options={durationOptions}
                autoFocus={true}
                className='select'
                onChange={(duration) => setDuration(duration.value)}
              />
              <div className='buttons'>
                  <button onClick={handleDemandClick}>Прогноз спроса</button>
                  <button onClick={handleOptimalPriceClick}>Подбор оптимальной цены</button>
              </div>

          </div>
          {render()}
        </>
    );
}

export default Chart;
