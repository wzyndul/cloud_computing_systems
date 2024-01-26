import React from 'react';

const Storage = () => {
    return (
    <div className={'storage-container'}>
      <h1>Stored Files</h1>
        <table className={'table'}>
            <thead>
                <tr>
                    <th>File Description</th>
                    <th>Previous Versions</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>File Name</td>
                    <td>File Type</td>
                </tr>
            </tbody>
        </table>
    </div>
  );
}

export default Storage;