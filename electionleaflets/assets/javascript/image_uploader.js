(function () {
  FilePond.registerPlugin(FilePondPluginImagePreview);
  FilePond.registerPlugin(FilePondPluginImageExifOrientation);
  const fileInput = document.querySelector('input[type="file"]');
  if (fileInput !== null) {
    const form = fileInput.closest('form');


    form.addEventListener('submit', function (e) {
      e.preventDefault();
      form.querySelector('button').setAttribute('disabled', true);
      pond.processFiles().then(function (uploaded_files) {
        const input_name = fileInput.name
        var hiddenS3Input = document.createElement('input');
        hiddenS3Input.type = 'hidden';
        hiddenS3Input.name = 's3file';
        form.appendChild(hiddenS3Input);

        var input_value = Array.from(document.querySelectorAll('input[name="' + input_name + '"]'));
        var all_values = [];
        uploaded_files.forEach(function (uploaded_file) {
          all_values.push(uploaded_file.serverId);
        })
        hiddenS3Input.value = JSON.stringify(input_value.map(function (input) {
          return input.name
        }));
        input_value.map(function (input) {
          input.value = JSON.stringify(all_values)
        })
        form.submit();
      });

    })
  }

  function parseKeyFromXML (xml_text) {
    var xml = new window.DOMParser().parseFromString(xml_text, 'text/xml')
    var tag = xml.getElementsByTagName('Key')[0]
    return decodeURI(tag.childNodes[0].nodeValue)
  }

  var fp_options = {
    imagePreviewTransparencyIndicator: 'grid',
    dropOnPage: true,
    labelIdle: "Take a photo of a leaflet",
    maxFiles: 10,
    instantUpload: false,
    oninit: function() {
      document.querySelector(".cta-row").style.display = 'none';
    },
    onaddfile: function() {
      document.querySelector(".cta-row").style.display = '';
      document.querySelector(".cta-row").querySelector("button").innerText = "Continue";
      window.pond.labelIdle = "Add another image of this leaflet";
    },
    server: {
      timeout: 5,
      process: function (fieldName, file, metadata, load, error, progress, abort, transfer, options) {
        // Create a new FormData object that will be POSTed to S3
        const s3Data = new FormData();

        // Loop over the input field attributes set by S3File
        // and add them to the FormData
        Array.from(fileInput.attributes).forEach(function (attr) {
          var name = attr.name
          if (name.startsWith('data-fields')) {
            name = name.replace('data-fields-', '')
            s3Data.append(name, attr.value)
          }
        });
        s3Data.append('success_action_status', '201');
        s3Data.append('Content-Type', file.type);
        s3Data.append('file', file);

        var url = fileInput.dataset.url;
        const request = new XMLHttpRequest();
        request.open('POST', url);

        request.upload.onprogress = (e) => {
          progress(e.lengthComputable, e.loaded, e.total);
        };

        request.onload = function() {
          if (request.status >= 200 && request.status < 300) {
            // the load method accepts either a string (id) or an object
            key = parseKeyFromXML(request.responseText);
            load(key);
          }
          else {
            // Can call the error method if something is wrong, should exit after
            error('oh no');
          }
        };

        request.send(s3Data);

        return {
          abort: () => {
            // This function is entered if the user has tapped the cancel button
            request.abort();

            // Let FilePond know the request has been cancelled
            abort();
          }
        };
      }
    }
  }

  const pond = FilePond.create( fileInput, fp_options);
  window.pond = pond;



})();
