const USERID = "id" + Math.random().toString(16).slice(2)
let selectedFiles = {}
const maxFiles = 5
const mbSize = 50
const maxSize = mbSize * 1024 * 1024


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
$("body").on("change", "#mediaFile", function(e){
    let filesLength = e.target.files.length
    for(let i = 0; i < filesLength; i++){
        if(Object.keys(selectedFiles).length > maxFiles){
            sendAlert(`<strong>Sorry! you have reached the maximum file limit</strong> `, 
            $(".response"), 10000 )
            return
        }
        let file_ = e.target.files[i]
        let splitName = file_.name.split(".")
        let ext = splitName.length > 0 ? splitName[splitName.length - 1] : ""
        if(file_.size > maxSize){
            sendAlert(`<strong>The maximum size for file uploads is ${mbSize} </strong> `, 
            $(".response"), 5000 )
            continue
        }
        if(!FORMATS.includes(ext.toLowerCase())){
            continue
        }
        // if(file_.name in selectedFiles){ }
        if(selectedFiles.hasOwnProperty(file_.name) === false){
            $(".upload-items").append(`
                <div data-itemname="${file_.name}" class="upload-item">
                    <div class="upload-item-detail">
                        ${file_.name}
                        <p class="text-danger"></p>
                        <!-- <div class="loading-effect"><div class="bar"></div></div> -->
                    </div>
                    <ul>
                        <li title="Delete" class="remove-file"><span><i class="fa fa-regular fa-trash"></i></span></li>
                        <li title="Conversion Completed"><span><i class="fa-solid fa-check fa"></i></span></li>
                        <li title="Download File" class="download-file"><span><i class="fa-solid fa-download fa"></i></span></li>
                    </ul>
                </div>
            `)
        }
        selectedFiles[file_.name] = file_
    }
})
$("body").on("click", ".remove-file", function(e){
    let grandParent = $(this).parent(0).parent(0);
    let filename = grandParent.data("itemname")
    delete selectedFiles[filename]
    grandParent.remove();
});
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
    $("#convertButton").attr("disabled", true)
    $(".conversion-success-responce").fadeOut()
    for(filename in selectedFiles){
        let file = selectedFiles[filename]
        let splitName = file.name.split(".")
        let ext = splitName.length > 0 ? splitName[splitName.length - 1] : ""
        let fileRowDiv = $('div[data-itemname="'+filename+'"]')
        let fileRowChildDiv = fileRowDiv.children("div").eq(0)
        if(ext == ""){
            fileRowChildDiv.children("p").eq(0).text("Unknown Format")
            continue
        }
        if(ext == convertTo){
            fileRowChildDiv.children("p").eq(0).text("You can not convert to the same format")
            continue
        }
        let formData = new FormData()
        formData.append("converter", converter)
        formData.append("convertTo", convertTo)
        formData.append("file", file)
        formData.append("file-name", filename)
        formData.append("file-format", ext)
        fileRowDiv.children("ul").eq(0).children("li").eq(1).css("display", "none")
        fileRowDiv.children("ul").eq(0).children("li").eq(2).css("display", "none")
        fileRowChildDiv.children("p").eq(0).fadeOut()
        fileRowChildDiv.append(`<div class="loading-effect"><div class="bar"></div></div>`)        
        await asyncPostQuery(formData, baseUrl+'media-converter').then((response) => {
            fileRowDiv.children("ul").eq(0).children("li").eq(1).css("display", "inline-block")
            fileRowDiv.children("ul").eq(0).children("li").eq(2).css("display", "inline-block")
            fileRowDiv.children("ul").eq(0).children("li").eq(2).attr("data-downloadlink", response.file_url)
            fileRowChildDiv.children("p").eq(0).removeClass("text-danger")
            fileRowChildDiv.children("p").eq(0).addClass("text-success")
            fileRowChildDiv.children("p").eq(0).text("Completed")
            successCounter++;
        }).catch((error) => {
            fileRowChildDiv.children("p").eq(0).addClass("text-danger")
            fileRowChildDiv.children("p").eq(0).removeClass("text-success")
            if (error.responseJSON != undefined && error.responseJSON != 'undefined'){
                fileRowChildDiv.children("p").eq(0).text(error.responseJSON.msg)
            }else{
                fileRowChildDiv.children("p").eq(0).text("An error occured")
            } 
        });
        fileRowChildDiv.children("p").eq(0).fadeIn()
        fileRowChildDiv.children("div.loading-effect").eq(0).remove()
    }
    $("#convertButton").attr("disabled", false)
    if(successCounter > 1){
        $(".conversion-success-responce").fadeIn()
    }
});
$("body").on("click", "#downloadConvertedFiles", async function(e){
    $("#downloadConvertedFiles").attr("disabled", true)
    let selectFiles = $("li.download-file")
    let filesTotal = selectFiles.length
    let converter = $("#converter").val()
    if(filesTotal < 1){
        $("#downloadConvertedFiles").attr("disabled", false)
        return
    }
    let form = new FormData()
    form.append("converter", converter)
    let filesCounter = 0
    for(let i = 0; i < filesTotal; i++){
        let row = i;
        let fileLink = selectFiles.eq(row).attr("data-downloadlink")
        let splitFileLink = fileLink.split("audio/")
        if(converter == "video-converter"){
            splitFileLink = fileLink.split("video/")
        }else if(converter == "audio-converter"){
            splitFileLink = fileLink.split("audio/")
        }else if(converter == "image-converter"){
            splitFileLink = fileLink.split("image/")
        }        
        let fileName = splitFileLink.length > 0 ? splitFileLink[splitFileLink.length - 1] : ""
        if(fileName != ""){
            form.append("files_links[]", fileName)
            filesCounter++
        }
    }
    if (filesCounter < 1){
        sendAlert(`<strong>No files to download</strong> `, 
        $(".response"), 10000 )
        $("#downloadConvertedFiles").attr("disabled", false)
        return
    }
    console.log("Files: ", selectFiles)
    await asyncPostQuery(form, baseUrl+'bulk-files-download').then((response) => {
        $("#downloadConvertedFiles").attr("disabled", false)
    //    location.href = response.download_url
    }).catch((error) => {
        if (error.responseJSON != undefined && error.responseJSON != 'undefined'){
            sendAlert(`<strong>${error.responseJSON.msg}</strong> `, $(".response"), 10000 )
        }else{
            sendAlert(`<strong>An error occured</strong> `, $(".response"), 10000 )
        } 
    });
    $("#downloadConvertedFiles").attr("disabled", false)
})
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