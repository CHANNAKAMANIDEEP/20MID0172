const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');

const app = express();
const PORT = 9876;
const WINDOW_SIZE = 10;

let windowNumbers = [];

app.use(bodyParser.json());

// API endpoint for fetching numbers from the test server
app.get('/numbers/:numberid', async (req, res) => {
  const { numberid } = req.params;
  
  try {
    const response = await axios.get(`http://localhost:9876/numbers/e/${numberid}`);
    const newData = response.data.filter(num => !windowNumbers.includes(num));
    const oldestNumber = windowNumbers.shift();
    windowNumbers.push(...newData);
    
    const windowPrevState = [...windowNumbers];
    const windowCurrState = [...windowNumbers];
    const avg = calculateAverage(windowNumbers);
    
    res.json({
      numbers: response.data,
      windowPrevState,
      windowCurrState,
      avg
    });
  } catch (error) {
    console.error("Error fetching data from the test server:", error.message);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

function calculateAverage(numbers) {
  const sum = numbers.reduce((acc, curr) => acc + curr, 0);
  return sum / numbers.length;
}

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});