import React, { Fragment } from "react";

import StudentResources from "./StudentResources";

export default function ContentNav() {
  return (
    <Fragment>
      <ul className="nav nav-tabs">
        <li className="nav-item">
          <a className="nav-link active" data-toggle="tab" href="#course1">
            Course 1
          </a>
        </li>
        <li className="nav-item">
          <a className="nav-link" data-toggle="tab" href="#course2">
            Course 2
          </a>
        </li>
        <li className="nav-item">
          <a className="nav-link" href="#course3">
            Course 3
          </a>
        </li>
      </ul>
      <div id="course2" className="tab-content">
        <div className="tab-pane fade active show" id="course1">
          <StudentResources />
        </div>
        <div className="tab-pane fade" id="course2">
          <p>
            Food truck fixie locavore, accusamus mcsweeney's marfa nulla
            single-origin coffee squid. Exercitation +1 labore velit, blog
            sartorial PBR leggings next level wes anderson artisan four loko
            farm-to-table craft beer twee. Qui photo booth letterpress, commodo
            enim craft beer mlkshk aliquip jean shorts ullamco ad vinyl cillum
            PBR. Homo nostrud organic, assumenda labore aesthetic magna delectus
            mollit.
          </p>
        </div>
      </div>
    </Fragment>
  );
}
