function formtoJSON(input){
        const formData = new FormData(input);
        const object = {};
        formData.forEach((value, key) => {object[key] = value});
        const json = JSON.stringify(object);
        return json;
}

function postRequest(data, endpoint) {
  const xhr = new XMLHttpRequest();
  xhr.open('POST', endpoint);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(data);
  return xhr;
}

function setCookie(name, value, expirationInDays) {
  const expirationDate = new Date();
  expirationDate.setTime(expirationDate.getTime() + expirationInDays * 24 * 60 * 60 * 1000);
  const expirationString = `expires=${expirationDate.toUTCString()}`;
  document.cookie = `${name}=${value};${expirationString};path=/`;
}

function getCookie(name) {
  const nameEQ = `${name}=`;
  const cookieArray = document.cookie.split(";");
  for (let i = 0; i < cookieArray.length; i++) {
    let cookie = cookieArray[i];
    while (cookie.charAt(0) === " ") {
      cookie = cookie.substring(1, cookie.length);
    }
    if (cookie.indexOf(nameEQ) === 0) {
      return cookie.substring(nameEQ.length, cookie.length);
    }
  }
  return null;
}
