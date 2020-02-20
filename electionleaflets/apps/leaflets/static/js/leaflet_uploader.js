var getCookie = function(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};
var handleError = function(err) {
    console.debug(err)
  var error = '<h2>Sorry, something has gone wrong</h2> <p>If the problem continues, ';
  error += '<a href="mailto:pollingstations@democracyclub.org.uk">contact us</a>.</p>';
  document.getElementById("error").innerHTML = error;
  document.getElementById("error").hidden = false;
  document.getElementById("submit").disabled = false;
};
var serializeFile = function(file) {
  if (file == null) return null;
  return {
    name: file.name,
    size: file.size,
    type: file.type,
  };
};
var getPresignedPostData = function() {
  return new Promise(function(resolve, reject) {
    var xhr = new XMLHttpRequest();
    var url = '{% url "file_upload_index" %}';
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    var payload = {
      files: [
        serializeFile(document.getElementById('id_front-image').files[0]),
      ].filter(Boolean),
      upload_session_id: document.getElementById('upload_session_id').value
    };
    xhr.send(JSON.stringify(payload));
    xhr.onload = function() {
      if (this.status === 200) {
        resolve(JSON.parse(this.responseText));
       } else {
        reject(this.responseText);
       }
    };
  });
};
var uploadFileToS3 = function(presignedPostData, file, progressBar) {
  return new Promise(function(resolve, reject) {
    var formData = new FormData();
    Object.keys(presignedPostData.fields).forEach(function(key) {
      formData.append(key, presignedPostData.fields[key]);
    });
    formData.append("file", document.getElementById(file).files[0]);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", presignedPostData.url, true);
    xhr.upload.addEventListener("progress", function(event) {
      document.getElementById(progressBar).value = (event.loaded / event.total) * 100;
    }, false);
    xhr.send(formData);
    xhr.onload = function() {
      if (this.status === 204) {
        resolve(this.responseText);
      } else {
        reject(this.responseText);
      }
    };
  });
};
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('file_upload_form').addEventListener("submit", function (e) {
    e.preventDefault();
    document.getElementById("error").innerHTML = "";
    document.getElementById("error").hidden = true;
    document.getElementById("submit").disabled = true;
    getPresignedPostData().then(
      function(data) {
        var uploads = [];
        for (var i=0; i<data.files.length; i++) {
          uploads.push(
            uploadFileToS3(data.files[i], 'id_front-image', 'progressBar0')
          );
        }
        Promise.all(uploads).then(
          function(data) {
            console.log('done!');
            console.log(data);
            document.getElementById("submit").disabled = false;

          },
          handleError
        );
      },
      handleError
    );
  });
});
