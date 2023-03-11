import React, { useState, useEffect, Fragment } from "react";
import axios from "axios";

export default function StudentResources(props) {
  const [students, setStudent] = useState([]);

  useEffect(() => {
    axios.get(`/ec2`).then((res) => {
      setStudent(res.data);
    });
  }, []);

  function buttonStatus(status) {
    console.log(status);
    if (status) {
      return <i className="fa fa-check-circle milestone-success"></i>;
    }
    return <i className="fa fa-exclamation-circle"></i>;
  }

  return (
    <Fragment>
      <table className="table table-striped">
        <thead className="thead-dark">
          <tr>
            <th scope="col">Student</th>
            <th scope="col">M1</th>
            <th scope="col">M2</th>
          </tr>
        </thead>
        <tbody>
          {students.map((student) => (
            <tr>
              <th scope="row">{student.name}</th>
              <td title={student.message}>
                {buttonStatus(student.is_success)}
              </td>
              <td>
                <i className="fa fa-exclamation-circle"></i>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </Fragment>
  );
}
