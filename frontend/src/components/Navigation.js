import React, { Fragment } from "react";

export default function Navigation(props) {
  return (
    <Fragment>
      <nav className="navbar navbar-expand navbar-light bg-light">
        <a className="navbar-brand" href="#">
          Lamarr
        </a>
        <ul className="navbar-nav mr-auto">
          <li className="nav-item active">
            <a className="nav-link" href="#">
              Lab 1 <span className="sr-only">(current)</span>
            </a>
          </li>
          <li>
            <a className="nav-link" href="#">
              Lab 2 <span className="sr-only">(current)</span>
            </a>
          </li>
          <li>
            <a className="nav-link" href="#">
              Lab 3 <span className="sr-only">(current)</span>
            </a>
          </li>
          <li>
            <a className="nav-link" href="#">
              Lab 4 <span className="sr-only">(current)</span>
            </a>
          </li>
        </ul>
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => window.location.reload(false)}
        >
          <i className="fa fa-refresh"></i> Refresh
        </button>
      </nav>
    </Fragment>
  );
}
