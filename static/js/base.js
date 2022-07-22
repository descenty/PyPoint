function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

const baseHeaders = new Headers();
baseHeaders.append('Content-Type', 'application/json');
baseHeaders.append('X-CSRFToken', getCookie('csrftoken'))
