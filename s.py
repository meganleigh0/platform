class MBOMPipeline:
    def __init__(self, variant):
        self.variant = variant
        self.df = None
        self.nodes = None

    def run(self):
        self.load_mbom()
        self.preprocess()
        self.standardize()
        self.structure()
        return self.df

    def load_mbom(self):
        # Implementation of load_mbom
        pass

    def preprocess(self):
        # Combine preprocessing steps into a single method
        self.clean_description()
        self.remove_unwanted_rows()
        self.set_ids()

    def clean_description(self):
        # Implementation
        pass

    def remove_unwanted_rows(self):
        # Implementation
        pass

    def set_ids(self):
        # Implementation
        pass

    def standardize(self):
        # Combine standardization steps
        self.assign_station_point()
        self.search_swh()

    def assign_station_point(self):
        # Implementation
        pass

    def search_swh(self):
        # Implementation
        pass

    def structure(self):
        # Convert data to final structure
        self.build_tree()
        self.propagate_station()
        self.tree_to_df()

    def build_tree(self):
        # Implementation
        pass

    def propagate_station(self):
        # Implementation
        pass

    def tree_to_df(self):
        # Convert the tree back to DataFrame
        pass
