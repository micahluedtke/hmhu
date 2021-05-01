// Initialize the FirebaseUI Widget using Firebase.
var ui = new firebaseui.auth.AuthUI(firebase.auth());

// As httpOnly cookies are to be used, do not persist any state client side.
firebase.auth().setPersistence(firebase.auth.Auth.Persistence.NONE);

// Exchange Client ID for Session Token
function convertClientIDToSessionToken(authResult){
  return authResult.user.getIdToken().then(idToken => {
    console.log(idToken);
    // Session login endpoint is queried and the session cookie is set.
    fetch('/auth/token', {
      method: 'POST',
      cache: 'no-cache', 
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: "include",
      referrerPolicy: 'no-referrer',
      body: JSON.stringify({ idToken: idToken })
    }).then(response => {
        if( response.ok ) return response.json();
        console.error(response);
      })
      .then(data => {
        if (data.hasOwnProperty('status')
          && data.status != undefined
          && data.status == "success" ){
          window.location.assign('/finishSignUp'); // reroute after login
        }
      });
  });
}

ui.start('#firebaseui-auth-container', {
  signInSuccessUrl: '/',
  signInOptions: [
    {
      provider: firebase.auth.EmailAuthProvider.PROVIDER_ID,
    }
  ],
  callbacks: {
    signInSuccessWithAuthResult: function(authResult, redirectUrl) {
      // User successfully signed in.
      convertClientIDToSessionToken(authResult);
      return false;
    },
    uiShown: function() {
      // The widget is rendered.
      // Hide the loader.
      document.getElementById('loader').style.display = 'none';
    }
  },
});