//22011032_Jacob_Craig_

// THIS PART OF THE CODE ENSURES USER CAN ONLY SELECT 90 ADVANCE BOOKINGS AND CANNOT SELECT DAYS BEFORE TODAY (THE CURRENT DAY)

// Get the current date
const today = new Date();

// Calculate the date 90 days from today
const maxDate = new Date();
maxDate.setDate(today.getDate() + 90);

// Format the dates as strings in the format required by the date input element
const todayDateString = today.toISOString().slice(0, 10);
const maxDateString = maxDate.toISOString().slice(0, 10);

// Set the minimum and maximum dates allowed in the date input element
const departDate = document.getElementById("departDate");
departDate.min = todayDateString;
departDate.max = maxDateString;





// THIS PART OF THE CODE ONLY ALLOWS THE RETURN DATE TO BE GREATER THAN THE DEPARTURE DATE

const returnDate = document.getElementById("returnDate");

departDate.addEventListener("change", function() {
  // Get the departure date from the departDate
  const departureDate = new Date(departDate.value);

  // Get the current return date
  const currentReturnDate = new Date(returnDate.value);

  // If the current return date is earlier than the departure date, reset the return date to the departure date
  if (currentReturnDate < departureDate) {
    returnDate.value = departDate.value;
  }
});

returnDate.addEventListener("change", function() {
  // Get the departure date from the departDate
  const departureDate = new Date(departDate.value);

  // Get the current return date
  const currentReturnDate = new Date(returnDate.value);

  // If the current return date is earlier than the departure date, reset the return date to the departure date
  if (currentReturnDate < departureDate) {
    returnDate.value = departDate.value;
  }
});



// THIS PART OF THE CODE ONLY WILL ALLOW THE RETURING DATE BOX TO BE ACTIVE IF ROUNDTRIP IS SELECTED - DISABLING WHEN ONE WAY IS SELECTED

function checkTravelType() {
  //alert("func called");
  var oneWay = document.getElementById("one-way");
  var roundTrip = document.getElementById("roundtrip");
  var returnDateBox = document.getElementById("returnDate");

  // returnDateBox.disabled = oneWay.checked ? true : false;
  if (oneWay.checked) {
    returnDateBox.disabled = true;
    returnDateBox.value = null;
    returnDateBox.style.color = "#c0c0c0";  // change text color to gray
    returnDateBox.style.border = "1px solid #c0c0c0";  // add a gray border;
  } else {
    returnDateBox.disabled = false;
    returnDateBox.style.color = "";  // reset text color
    returnDateBox.style.border = "";  // remove border
  }

}



// THIS PART OF THE CODE GETS CORRESPONDING TRAVELLING LOCATIONS BASED ON SELECTED DEPATURE LOCATION

 function getarrivalcity(deptcity)    
{
     console.log('passed val = ' + deptcity);
     var req = new XMLHttpRequest();        
     arrivalslist = document.getElementById('arrivalslist');        
     
     req.onreadystatechange = function(){
         if (req.readyState == 4){
             if (req.status != 200){
                 //error handling code here
             }
             else{
                 var response = JSON.parse(req.responseText);                   
                 //document.getElementById('myDiv').innerHTML = response.username
                 var size = response.size;                   
                 //alert(response.returncities[0]);
                 //console.log(arrivalslist);
                 for (var x=0; x < arrivalslist.length; x++){
                     arrivalslist.remove(x);                        
                 }
                 
                 for (var i=0; i < size; i++){  

                         arrivalslist.add(new Option(response.returncities[i], response.returncities[i]));    
                 }
                    // var option = document.createElement("Option");
                     //option.text = response.returncities;
                     //arrivalslist.add(option);
             }
         }
     }
     req.open('GET', '/returncity/?q='+deptcity);
     req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");   
     req.send(); 
     return false;
 }


// THIS PART OF THE CODE ENSURES THAT THE USER CANNOT SELECT A SUNDAY AS A DEPARTURE OR RETURN DATE (AIR TRAVEL IS NOT ALLOWED ON SUNDAYS)

// Get the form and the depart and return date input fields
const form = document.getElementById("flightForm");
const departDateInput = document.getElementById("departDate");
const returnDateInput = document.getElementById("returnDate");

// Function to check if a date is a Sunday
function isSunday(date) {
  return date.getDay() === 0;
}

// Function to handle form submission
function handleSubmit(event) {
  // Prevent the default form submission behavior
  event.preventDefault();

  // Check if departDate is on a Sunday
  if (isSunday(new Date(departDateInput.value))) {
    // Display an alert
    alert("Departure date cannot be on a Sunday");
    return;
  }

  // Check if returnDate is on a Sunday (if it's not a one-way flight)
  if (returnDateInput.value && isSunday(new Date(returnDateInput.value))) {
    // Display an alert
    alert("Return date cannot be on a Sunday");
    return;
  }

  //check if is is return flight, if so, check if return date is filled
  if (returnDateInput.value == "" && document.getElementById("roundtrip").checked) {
    // Display an alert
    alert("Return date cannot be empty");
    return;
  }
  

  // If we got this far, the dates are valid, so submit the form
  form.submit();
}

// Add an event listener for form submission
form.addEventListener("submit", handleSubmit);
