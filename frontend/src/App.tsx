import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGithub } from '@fortawesome/free-brands-svg-icons';

import './App.css';


function App() {
  interface Package {
    name: string;
    version: string;
  }
  
  interface ComparisonResult {
    same: Package[];
    different: [Package, Package][];
    only_in_first: Package[];
    only_in_second: Package[];
  }

  const [file1, setFile1] = useState<File | null>(null);
  const [file2, setFile2] = useState<File | null>(null);
  const [result, setResult] = useState<ComparisonResult | null>(null);

  const compareRequirements = async () => {
    if (!file1 || !file2) {
      alert('Please select both files before comparing.');
      return;
    }

    const formData = new FormData();
    formData.append('file1', file1);
    formData.append('file2', file2);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/compare', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: ComparisonResult = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
      alert(`An error occurred while fetching the data: ${error}`);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>, setFile: React.Dispatch<React.SetStateAction<File | null>>) => {
    const file = event.target.files?.[0];
    if (file) {
      setFile(file);
    }
  };

  return (
    <div className="App">
      <div className="hero-section">
        <nav className="navbar">
          <h1>Python Requirements Comparison</h1>
        </nav>
        <header className="App-header">
          <h2>Compare Your Requirements Files</h2>
          <p>
            Find differences in package versions, identify missing dependencies, and spot unique packages in each file.<br />
            Comparison tool supports various formats, including those generated by <code>pip freeze</code>
          </p>
        </header>
      </div>

      <main>
        <div className="upload-section">
          <div className="upload-card">
            <h3>Base Requirements</h3>
            <input type="file" onChange={(e) => handleFileChange(e, setFile1)} />
            {file1 && <p>Selected file: {file1.name}</p>}
          </div>
          <div className="upload-card">
            <h3>Comparison Requirements</h3>
            <input type="file" onChange={(e) => handleFileChange(e, setFile2)} />
            {file2 && <p>Selected file: {file2.name}</p>}
          </div>
        </div>
        <div className="compare-button-container">
            <button className="compare-button" onClick={compareRequirements}>
              Compare
            </button>
        </div>
        {result && (
          <div className="result">
            <h3 className="comparison-result-heading">Comparison Result:</h3>
            <div className="result-tables">
              <table>
                <thead>
                  <tr>
                    <th>{file1 ? file1.name : 'File 1'}</th>
                    <th>{file2 ? file2.name : 'File 2'}</th>
                  </tr>
                </thead>
                <tbody>

                  {result.same.map((pkg, index) => (
                    <tr key={`same-${index}`}>
                      <td>{pkg.name} {pkg.version}</td>
                      <td>{pkg.name} {pkg.version}</td>
                    </tr>
                  ))}
                  {result.different.map((pkg, index) => (
                    <tr key={`diff-${index}`}>
                      <td>{pkg[0].name} {pkg[0].version}</td>
                      <td>{pkg[1].name} {pkg[1].version}</td>
                    </tr>
                  ))}
                  {result.only_in_first.map((pkg, index) => (
                    <tr key={`first-${index}`}>
                      <td>{pkg.name} {pkg.version}</td>
                      <td>-</td>
                    </tr>
                  ))}
                  {result.only_in_second.map((pkg, index) => (
                    <tr key={`second-${index}`}>
                      <td>-</td>
                      <td>{pkg.name} {pkg.version}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
        <div className="footer-spacer"></div>
      </main>

      <footer>
        <p>
          © 2024 Python Requirements Comparison Tool. 
          <a 
            href="https://github.com/Sebastvin" 
            target="_blank" 
            rel="noopener noreferrer"
            style={{ marginLeft: '10px', color: 'inherit', textDecoration: 'none' }}
          >
            <FontAwesomeIcon icon={faGithub} />
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
