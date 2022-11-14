function InitializeTeacherInfo() {
    
    var request = new XMLHttpRequest()

    request.open('GET', 'http://127.0.0.1:5000/Teacher', true)
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
                } else {
                    var temp = data[Object.keys(data)[i]];
                    var arr = temp.split("|");
                    
                    var row = table.insertRow();
                    var cell1 = row.insertCell(0);
                    var cell2 = row.insertCell(1);
                    var cell3 = row.insertCell(2);
                    var cell4 = row.insertCell(3);

                    let button = document.createElement("button");
                    button.innerHTML = Object.keys(data)[i];
                    button.id = Object.keys(data)[i];

                    button.onclick = function getClassInfo(){
                        location.replace("TeacherViewClass.html")
                        
                        var request1 = new XMLHttpRequest()

                        request1.open('GET', 'http://127.0.0.1:5000/Teacher/SetCourse/' + String(button.id), true)

                        request1.send()
                    }

                    cell1.append(button);
                    cell2.innerHTML = arr[1];
                    cell3.innerHTML = arr[2];
                    cell4.innerHTML = arr[3] + "/" + arr[4];
                }

            }        

        }
    }

    request.send()

}

function LogOut() {
    location.replace("HomeLanding.html");
}
