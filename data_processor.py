import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class DataProcessor:
    def __init__(self, csv_path: str = None):
        """Initialize the data processor with the path to the CSV file."""
        self.csv_path = csv_path
        self.df = None
        if csv_path:
            self.load_data()
    
    def _get_naics_columns(self, columns):
        """Find the NAICS code and title columns regardless of year."""
        naics_code_col = next((col for col in columns if 'NAICS Code' in col), None)
        naics_title_col = next((col for col in columns if 'NAICS Title' in col), None)
        return naics_code_col, naics_title_col
    
    def load_data(self):
        """Load and preprocess the CSV data."""
        try:
            # Read the CSV file in chunks due to its large size
            chunks = []
            for chunk in pd.read_csv(self.csv_path, chunksize=10000, low_memory=False):
                # Basic preprocessing for each chunk
                chunk = chunk.fillna(0)
                chunks.append(chunk)
            
            if not chunks:
                raise ValueError("No data could be loaded from the CSV file")
                
            self.df = pd.concat(chunks, ignore_index=True)
            
            # Get NAICS columns
            naics_code_col, naics_title_col = self._get_naics_columns(self.df.columns)
            if not naics_code_col or not naics_title_col:
                raise ValueError("Could not find NAICS Code and Title columns")
            
            # Store column names for later use
            self.naics_code_col = naics_code_col
            self.naics_title_col = naics_title_col
            
            # Validate required columns
            required_columns = [
                naics_code_col, naics_title_col, 'GHG', 'Unit',
                'Supply Chain Emission Factors without Margins',
                'Margins of Supply Chain Emission Factors',
                'Supply Chain Emission Factors with Margins'
            ]
            
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Convert NAICS codes to string type for consistent handling
            self.df[naics_code_col] = self.df[naics_code_col].astype(str)
            
            # Verify data integrity
            if len(self.df) == 0:
                raise ValueError("No valid data after preprocessing")
                
            print(f"Successfully loaded {len(self.df)} records")
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            self.df = None
            raise

    def load_from_upload(self, uploaded_file):
        """Load data from an uploaded CSV file."""
        temp_path = None
        try:
            # Save the uploaded file temporarily
            temp_path = "temp_upload.csv"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Update the csv_path and load the data
            self.csv_path = temp_path
            self.load_data()
            
            return True
        except Exception as e:
            print(f"Error loading uploaded file: {str(e)}")
            return False
        finally:
            # Clean up the temporary file
            if temp_path:
                try:
                    import os
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                except Exception as e:
                    print(f"Warning: Could not remove temporary file: {str(e)}")
    
    def get_emission_factors(self, naics_code: str = None) -> pd.DataFrame:
        """Get emission factors for a specific NAICS code or all codes."""
        if naics_code:
            return self.df[self.df[self.naics_code_col] == naics_code]
        return self.df
    
    def get_emission_summary(self) -> Dict:
        """Get summary statistics of emission factors."""
        try:
            if self.df is None:
                return {
                    'total_records': 0,
                    'unique_naics': 0,
                    'emission_stats': {}
                }
            
            # Get numeric columns excluding NAICS code
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            numeric_cols = [col for col in numeric_cols if 'NAICS' not in col]
            
            # Calculate summary statistics
            summary = {
                'total_records': int(len(self.df)),  # Convert to int for display
                'unique_naics': int(self.df[self.naics_code_col].nunique()),  # Convert to int for display
                'emission_stats': self.df[numeric_cols].describe().to_dict()
            }
            
            # Add column information
            summary['columns'] = {
                'naics_code_col': self.naics_code_col,
                'naics_title_col': self.naics_title_col,
                'numeric_cols': list(numeric_cols)
            }
            
            return summary
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return {
                'total_records': 0,
                'unique_naics': 0,
                'emission_stats': {},
                'error': str(e)
            }
    
    def search_naics(self, query: str) -> List[Tuple[str, str]]:
        """Search for NAICS codes and descriptions based on a query."""
        # Convert query to lowercase for case-insensitive search
        query = query.lower()
        
        # Search in NAICS codes and descriptions
        matches = self.df[
            self.df[self.naics_code_col].astype(str).str.contains(query, case=False) |
            self.df[self.naics_title_col].str.lower().str.contains(query, case=False)
        ]
        
        # Return list of (NAICS code, description) tuples
        return list(zip(matches[self.naics_code_col], matches[self.naics_title_col]))
    
    def get_emission_trends(self, naics_code: str) -> Dict:
        """Get emission trends for a specific NAICS code."""
        if naics_code not in self.df[self.naics_code_col].values:
            return {}
            
        naics_data = self.df[self.df[self.naics_code_col] == naics_code]
        
        # Calculate trends (assuming there are multiple years in the data)
        trends = {
            'naics_code': naics_code,
            'description': naics_data[self.naics_title_col].iloc[0],
            'emission_factors': naics_data.select_dtypes(include=[np.number]).mean().to_dict()
        }
        
        return trends 