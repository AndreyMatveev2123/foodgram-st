import "./fonts/SanFranciscoProDisplay/fonts.css";
import "./App.css";
import { Switch, Route, useHistory, Redirect } from "react-router-dom";
import React, { useState, useEffect } from "react";
import { Header, Footer, ProtectedRoute } from "./components";
import api from "./api";
import styles from "./styles.module.css";

import {
  About,
  Main,
  Cart,
  SignIn,
  Subscriptions,
  Favorites,
  SingleCard,
  SignUp,
  RecipeEdit,
  RecipeCreate,
  User,
  ChangePassword,
  NotFound,
  UpdateAvatar,
  ResetPassword,
  Technologies,
} from "./pages";

import { AuthContext, UserContext } from "./contexts";

function App() {
  const [loggedIn, setLoggedIn] = useState(null);
  const [user, setUser] = useState({});
  const [orders, setOrders] = useState(0);
  const [authError, setAuthError] = useState({ submitError: "" });
  const [registrError, setRegistrError] = useState({ submitError: "" });
  const [changePasswordError, setChangePasswordError] = useState({
    submitError: "",
  });

  const registration = ({
    email,
    password,
    username,
    first_name,
    last_name,
  }) => {
    api
      .signup({ email, password, username, first_name, last_name })
      .then(() => {
        history.push("/signin");
      })
      .catch((err) => {
        const errors = Object.values(err);
        if (errors) {
          setRegistrError({ submitError: errors.join(", ") });
        }
        setLoggedIn(false);
      });
  };

  const changePassword = ({ new_password, current_password }) => {
    api
      .changePassword({ new_password, current_password })
      .then((res) => {
        history.push("/signin");
      })
      .catch((err) => {
        const errors = Object.values(err);
        if (errors) {
          setChangePasswordError({ submitError: errors.join(", ") });
        }
      });
  };

  const changeAvatar = ({ file }) => {
    api
      .changeAvatar({ file })
      .then((res) => {
        setUser({ ...user, avatar: res.avatar });
        history.push(`/recipes`);
      })
      .catch((err) => {
        const { non_field_errors } = err;
        if (non_field_errors) {
          return alert(non_field_errors.join(", "));
        }
        const errors = Object.values(err);
        if (errors) {
          alert(errors.join(", "));
        }
      });
  };

  const authorization = ({ email, password }) => {
    api
      .signin({
        email,
        password,
      })
      .then((res) => {
        if (res.auth_token) {
          localStorage.setItem("token", res.auth_token);
          api
            .getUserData()
            .then((res) => {
              setUser(res);
              setLoggedIn(true);
              getOrders();
            })
            .catch((err) => {
              setLoggedIn(false);
              history.push("/signin");
            });
        } else {
          setLoggedIn(false);
        }
      })
      .catch((err) => {
        const errors = Object.values(err);
        if (errors) {
          setAuthError({ submitError: errors.join(", ") });
        }
        setLoggedIn(false);
      });
  };

  const onPasswordReset = ({ email }) => {
    api
      .resetPassword({
        email,
      })
      .then((res) => {
        history.push("/signin");
      })
      .catch((err) => {
        const errors = Object.values(err);
        if (errors) {
          alert(errors.join(", "));
        }
        setLoggedIn(false);
      });
  };

  const loadSingleItem = ({ id, callback }) => {
    setTimeout((_) => {
      callback();
    }, 3000);
  };

  const history = useHistory();
  const onSignOut = () => {
    api
      .signout()
      .then((res) => {
        localStorage.removeItem("token");
        setLoggedIn(false);
      })
      .catch((err) => {
        const errors = Object.values(err);
        if (errors) {
          alert(errors.join(", "));
        }
      });
  };

  const getOrders = () => {
    api
      .getRecipes({
        page: 1,
        is_in_shopping_cart: Number(true),
      })
      .then((res) => {
        const { count } = res;
        setOrders(count);
      });
  };

  const updateOrders = (add) => {
    if (!add && orders <= 0) {
      return;
    }
    if (add) {
      setOrders(orders + 1);
    } else {
      setOrders(orders - 1);
    }
  };

  useEffect((_) => {
    const token = localStorage.getItem("token");
    if (token) {
      return api
        .getUserData()
        .then((res) => {
          setUser(res);
          setLoggedIn(true);
          getOrders();
        })
        .catch((err) => {
          setLoggedIn(false);
          history.push("/recipes");
        });
    } else {
      setLoggedIn(false);
    }
  }, []);

  // useEffect(() => {
  //   document.addEventListener('keydown', function(event) {
  //     if (event.ctrlKey && event.shiftKey && event.key === 'z') {
  //       alert('зиги - добар пас!');
  //     }
  //   });
  // }, [])

  if (loggedIn === null) {
    return <div className={styles.loading}>Загрузка...</div>;
  }

  return (
    <AuthContext.Provider
      value={{
        loggedIn,
        setLoggedIn,
        authorization,
        registration,
        onSignOut,
        authError,
        registrError,
        changePassword,
        changePasswordError,
        onPasswordReset,
        changeAvatar,
      }}
    >
      <UserContext.Provider value={{ user, setUser, updateOrders, orders }}>
        <div className="App">
          <Header orders={orders} loggedIn={loggedIn} onSignOut={onSignOut} />
          <Switch>
            <Route exact path="/" component={Main} />
            <Route exact path="/signin" component={SignIn} />
            <Route exact path="/signup" component={SignUp} />
            <Route exact path="/cart" component={Cart} />
            <Route exact path="/subscriptions" component={Subscriptions} />
            <Route exact path="/favorites" component={Favorites} />
            <Route exact path="/recipes/:id" component={SingleCard} />
            <Route exact path="/recipes/:id/edit" component={RecipeEdit} />
            <Route exact path="/recipes/create" component={RecipeCreate} />
            <Route exact path="/user/:id" component={User} />
            <Route exact path="/change-password" component={ChangePassword} />
            <Route exact path="/update-avatar" component={UpdateAvatar} />
            <Route exact path="/reset-password" component={ResetPassword} />
            <Route exact path="/about" component={About} />
            <Route exact path="/technologies" component={Technologies} />
            <Route component={NotFound} />
          </Switch>
          <Footer />
        </div>
      </UserContext.Provider>
    </AuthContext.Provider>
  );
}

export default App;
