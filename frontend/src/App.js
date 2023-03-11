import React, { Fragment } from "react";
import "./BootstrapCosmo.css";
import "../node_modules/font-awesome/css/font-awesome.min.css";
import "./App.css";

import Navigation from "./components/Navigation";
import StudentResources from "./components/StudentResources";

export default function App(props) {
  return (
    <Fragment>
      <Navigation />
      <div className="container-md mt-5">
        <StudentResources />
      </div>
    </Fragment>
  );
}
