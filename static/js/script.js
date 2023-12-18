const USERID = "id" + Math.random().toString(16).slice(2)
let selectedFiles = {};
let maxFiles = 5;

$("body").on("submit", "#sendYoutubeVideoLink", function(event){
    event.preventDefault()
    let _this = $(this)
    let targetForm = this.closest('form');
    console.log("Form Submited", this.closest("form"))
    formData = new FormData(targetForm)
    formData.append("user-id", USERID)
    $.ajax({
        method: "POST",
        data: formData,
        url: "/download-youtube-videos",
        cache: false,
        contentType: false,
        processData: false,
        'beforeSend': function () {
            
        },
        'success': function (res) {
            console.log("Response: ", res)
        },
        'error': function (error) {
            if ( error.responseJSON != undefined && error.responseJSON != 'undefined'){
                sendAlert(error.responseJSON.msg, $(".response"), 21000, "alert-danger")
            }else{
                sendAlert("<strong>An error occured</strong>", $(".response"), 21000, "alert-danger")

            }  
        },
        'progress': function(evt){
            console.log(evt)
        }
    })
});
$("body").on("change", "#audioFile", function(e){
    if(Object.keys(selectedFiles).length >= maxFiles){
        sendAlert(`<strong>Sorry! you have reached the maximum file limit</strong> `, 
        $(".response"), 10000 )
        return
    }
    let filesLength = e.target.files.length
    for(let i = 0; i < filesLength; i++){
        let file_ = e.target.files[i]
        let splitName = file_.name.split(".")
        let ext = splitName[splitName.length - 1]
        if(!FORMATS.includes(ext)){
            continue;
        }
        // if(file_.name in selectedFiles){ }
        if(selectedFiles.hasOwnProperty(file_.name) === false){
            $(".upload-items").append(`
                <div data-itemname="${file_.name}" class="upload-item">
                    <div>${file_.name}
                    <p class="text-danger"></p>
                    </div>
                    <ul>
                        <li class="remove-file"><span><i class="fa fa-regular fa-trash"></i></span></li>
                        <li><span><i class="fa-solid fa-check fa"></i></span></li>
                        <li class="download-file"><span><i class="fa-solid fa-download fa"></i></span></li>
                    </ul>
                </div>
            `)
        }
        selectedFiles[file_.name] = file_;
    }
    console.log("Selected Files", selectedFiles);
})

$("body").on("click", "#convertButton", async function(e){
    if(Object.keys(selectedFiles).length < 1){
        sendAlert(`<strong>Please select at least one file to convert</strong> `, 
        $(".response"), 10000 )
        return
    }
    let converter = $("#converter").val()
    let convertTo = $("#convertTo").val()
    if(convertTo == ""){
        sendAlert(`<strong>Please select the conversion format</strong> `, 
        $(".response"), 10000 )
        return
    }
    if(converter == ""){
        sendAlert(`<strong>An error occured</strong> `, 
        $(".response"), 10000 )
        return
    }
    let successCounter = 0
    for(filename in selectedFiles){
        let file = selectedFiles[filename]
        let splitName = file.name.split(".")
        let ext = splitName[splitName.length - 1]
        let formData = new FormData()
        formData.append("converter", converter)
        formData.append("convertTo", convertTo)
        formData.append("file", file)
        formData.append("file-name", filename)
        formData.append("file-format", ext)
        let fileRowDiv = $('div[data-itemname="'+filename+'"]')
        fileRowDiv.children("ul").eq(0).children("li").eq(1).css("display", "none")
        fileRowDiv.children("ul").eq(0).children("li").eq(2).css("display", "none")
        fileRowDiv.children("div").eq(0).children("p").eq(0).text("")
        await asyncPostQuery(formData, baseUrl+'media-converter').then((response) => {
            fileRowDiv.children("ul").eq(0).children("li").eq(1).css("display", "inline-block")
            fileRowDiv.children("ul").eq(0).children("li").eq(2).css("display", "inline-block")
            fileRowDiv.children("ul").eq(0).children("li").eq(2).attr("data-downloadlink", response.file_url)
        }).catch((error) => {
            if (error.responseJSON != undefined && error.responseJSON != 'undefined'){
                fileRowDiv.children("div").eq(0).children("p").eq(0).text(error.responseJSON.msg)
                // sendAlert(error.responseJSON.msg, $(".response"), 21000, "alert-danger")
            }else{
                fileRowDiv.children("div").eq(0).children("p").eq(0).text("An error occured")
                // sendAlert("<strong>An error occured</strong>", $(".response"), 21000, "alert-danger")
            } 
        });
    }
    if(successCounter > 1)
        $(".conversion-success-responce").fadeIn()
});
$("body").on("click", ".download-file", function(e){
    downloadLink = $(this).data("downloadlink")
    location.href = downloadLink
})
const asyncPostQuery = async (formData, reqUrl) => {
    let _this = this;
    _this.data = null;
    _this.error = "";
    const queryMaker = async (form, link) => {
        console.log("LINK: ", link)
        return $.ajax({
            method: "POST",
            data: form,
            url: link,
            cache: false,
            contentType: false,
            processData: false,
            'success': function (res) {
               _this.data = res;
            },
            'error': function (error) {
                console.log("This error")
                _this.error = error; 
            }
        })
    }
    const processQuery = async (x) => {
        return new Promise((resolve, reject) => {
            if(_this.data)
                resolve(_this.data);
            else
                reject(_this.error)
        })
    }
    return await processQuery(await queryMaker(formData, reqUrl))
}
function sendAlert(message, alertElem, _duration=5000, alertType = 'alert-warning') {
    let html = ` <div class="alert ${alertType} alert-dismissible fade show" role="alert">
                        ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>`
    alertElem.html(html);      
    setTimeout(
        function(){
          $(".my-alart").fadeOut('slow');
        } , _duration
    );
}