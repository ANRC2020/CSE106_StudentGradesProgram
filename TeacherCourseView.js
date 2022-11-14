function InitializeCourseView() {
    
    var request = new XMLHttpRequest()

    request.open('GET', 'http://127.0.0.1:5000/Teacher/GetCourse', true)
    request.onload = function () {
        
        var data = JSON.parse(this.response)

        if (request.status >= 200 && request.status < 400) {
        
            var table = document.getElementById('Course Information');
            var teacher_name = []

            for (i in Object.keys(data)){
                // console.log(Object.keys(data)[i] + "\n" +  data[Object.keys(data)[i]] + "\n");
                
                if (parseInt(data[Object.keys(data)[i]]) >= 9000) {

                    teacher_name.push(Object.keys(data)[i]);      
                    const header = document.getElementById('Teacher Greeting');

                    header.innerHTML = "Hello Professor " + teacher_name + "!";
                } else if (data[Object.keys(data)[i]] == -1) {
                    document.getElementById('Class Name').innerHTML = Object.keys(data)[i];

                } else {
                    var temp = data[Object.keys(data)[i]];
                    
                    let text_box = document.createElement("input");
                    text_box.innerHTML = Object.keys(data)[i];
                    text_box.id = Object.keys(data)[i] + " text";
                    
                    let button = document.createElement("button");
                    button.innerHTML = "Submit";
                    button.id = Object.keys(data)[i];

                    button.onclick = function getClassInfo(){
                        var new_grade = document.getElementById(button.id + " text").value;

                        console.log(new_grade, button.id)

                        if (new_grade < 0) {
                            new_grade = 0;
                        }

                        const data = {"StudentName":button.id,"newGrade":new_grade};
                        
                        fetch("http://127.0.0.1:5000/Teacher/UpdateGrade",{
                            method:'PUT',
                            headers:{'Content-Type':'application/json'},
                            body:JSON.stringify(data)
                        })
                        .then(response=>response.json())
                    }
                    
                    var row = table.insertRow();
                    var cell1 = row.insertCell(0);
                    var cell2 = row.insertCell(1);
                    var cell3 = row.insertCell(2);

                    cell1.innerHTML = Object.keys(data)[i];
                    cell2.innerHTML = data[Object.keys(data)[i]];
                    cell3.append(text_box)
                    cell3.append(button)
                }

            }        

        }
    }

    request.send()

}

function Back() {
    location.replace("Teacher.html")
}