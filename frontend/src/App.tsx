import React, { useState } from 'react';
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
      <nav>
        <div className="navbar">
          <h1>Python Requirements Comparison</h1>
        </div>
      </nav>

      <header className="App-header">
        <h2>Compare Your Requirements Files</h2>
        <p>This tool allows you to compare two requirements documents to find differences and similarities.</p>
      </header>

      <main>
        <div className="upload-section">
          <div className="upload">
            <h3>Requirement 1</h3>
            <input type="file" onChange={(e) => handleFileChange(e, setFile1)} />
            {file1 && <p>Selected file: {file1.name}</p>}
          </div>
          <div className="upload">
            <h3>Requirement 2</h3>
            <input type="file" onChange={(e) => handleFileChange(e, setFile2)} />
            {file2 && <p>Selected file: {file2.name}</p>}
          </div>
        </div>
        <button onClick={compareRequirements}>Compare</button>
        {result && (
          <div className="result">
            <h3>Comparison Result:</h3>
            <div className="result-tables">
              <table>
                <thead>
                  <tr>
                    <th>File 1</th>
                    <th>File 2</th>
                  </tr>
                </thead>
                <tbody>
                  {/* Same packages */}
                  {result.same.map((pkg: any, index: number) => (
                    <tr key={`same-${index}`}>
                      <td>{pkg.name} {pkg.version}</td>
                      <td>{pkg.name} {pkg.version}</td>
                    </tr>
                  ))}
                  {/* Different packages */}
                  {result.different.map((pkg: any, index: number) => (
                    <tr key={`diff-${index}`}>
                      <td>{pkg[0].name} {pkg[0].version}</td>
                      <td>{pkg[1].name} {pkg[1].version}</td>
                    </tr>
                  ))}
                  {/* Only in first file */}
                  {result.only_in_first.map((pkg: any, index: number) => (
                    <tr key={`first-${index}`}>
                      <td>{pkg.name} {pkg.version}</td>
                      <td>None</td>
                    </tr>
                  ))}
                  {/* Only in second file */}
                  {result.only_in_second.map((pkg: any, index: number) => (
                    <tr key={`second-${index}`}>
                      <td>None</td>
                      <td>{pkg.name} {pkg.version}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>

      <footer>
        <p>© 2024 Python Requirements Comparison Tool. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
