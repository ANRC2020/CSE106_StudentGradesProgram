function ManageEnrollment() {

    var request = new XMLHttpRequest()

    request.open('GET', 'http://127.0.0.1:5000/Student/ManageEnrollment', true)
    request.onload = function () {

        var data = JSON.parse(this.response)

        if (request.status >= 200 && request.status < 400) {
            // console.log(data)

            var table = document.getElementById('Enrollment Information');

            for (i in Object.keys(data)){
                // console.log(data[Object.keys(data)[i]])
                var temp = data[Object.keys(data)[i]];
                var arr = temp.split(/(\s+)/);
                
                var row = table.insertRow();
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(3);
                var cell5 = row.insertCell(4);

                cell1.innerHTML = Object.keys(data)[i];
                cell2.innerHTML = arr[0] + arr[1] + arr[2];
                cell3.innerHTML = arr[4] + arr[5] + arr[6] + arr[7] + arr[8];
                cell4.innerHTML = arr[10] + "/" + arr[12]; 
                let button = document.createElement("button");
                // let td = document.createElement("td");
                
                button.innerText = arr[14];
                button.id = Object.keys(data)[i];
                
                if(button.innerText == "Add"){
                    button.onclick = function AddClass() {
                        console.log("Called Add Class!")
                        console.log(button.id)

                        const send_data = {"course":button.id};
                        
                        console.log(send_data)

                        fetch("http://127.0.0.1:5000/Student/ManageEnrollment/Add",{
                            method:'POST',
                            headers:{'Content-Type':'application/json'},
                            body:JSON.stringify(send_data)
                        })
                        .then(response=>response.json())                  
                    };

                } else if (button.innerHTML == "Drop") {
                    button.onclick = function DropClass() {
                        console.log("Called Drop Class!")
                        console.log(button.id)

                        const send_data = {"course":button.id, "num_students":arr[10]};

                        fetch("http://127.0.0.1:5000/Student/ManageEnrollment/Drop",{
                            method:'DELETE',
                            headers:{'Content-Type':'application/json'},
                            body:JSON.stringify(send_data)
                        })
                        .then(response=>response.json())
                    };
                }

                button.id = Object.keys(data)[i];
                cell5.append(button);          
            }

        }

    }

    request.send();
}

function InitializeStudentInfo() {

    var request = new XMLHttpRequest()
    var student_name = [];
    var courses = [];
    var course_times = [];

    request.open('GET', 'http://127.0.0.1:5000/Student', true)
    request.onload = function () {

        var data = JSON.parse(this.response)
        var found = 0

        if (request.status >= 200 && request.status < 400) {
            // console.log(data)

            var table = document.getElementById('Course Information');

            for (i in Object.keys(data)){
                // console.log(data[Object.keys(data)[i]])

                if(i == 0){
                    student_name.push(data[Object.keys(data)[i]]);
                    // console.log(student_name)                    
                    const header = document.getElementById('Student Greeting');

                    header.innerHTML = "Hello " + student_name + "!";
                } else {
                    var temp = data[Object.keys(data)[i]];
                    var arr = temp.split(/(\s+)/);
                    
                    var row = table.insertRow();
                    var cell1 = row.insertCell(0);
                    var cell2 = row.insertCell(1);
                    var cell3 = row.insertCell(2);
                    var cell4 = row.insertCell(3);
                    var cell5 = row.insertCell(4);

                    cell1.innerHTML = Object.keys(data)[i];
                    cell2.innerHTML = arr[0] + arr[1] + arr[2];
                    cell3.innerHTML = arr[4] + arr[5] + arr[6] + arr[7] + arr[8];
                    cell4.innerHTML = arr[10];
                    cell5.innerHTML = arr[12] + "/" + arr[14];

                    courses.push(cell1);
                    course_times.push(cell3);
                }                

            }

        }

    }

    request.send();

    ManageEnrollment();
}

function LogOut() {
    location.replace("HomeLanding.html");
}