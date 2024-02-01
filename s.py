    # Assuming other parts of the class remain the same
    def plant3_process(self, product):
        yield self.p1_processed  # Ensure Plant 1 processing is completed
        for station in self.hull_station_order:
            # Processing logic for each station as before
            # ...
        
        # New logic for waiting for marriage
        if not self.product.turret.p3_processed.triggered:
            # This hull is ready, but waiting for the turret
            self.env.process(self.wait_for_marriage(self.product.turret))
        else:
            # Both hull and turret are ready, proceed to marriage process
            self.env.process(self.product.marriage(self, self.product.turret))
        self.p3_processed.succeed()
    
    async def wait_for_marriage(self, other_component):
        """Wait for the other component to be ready for marriage."""
        yield other_component.p3_processed  # Wait for the turret's processing to be completed
        # Logic to pull the hull off the line can be added here
        self.env.process(self.product.marriage(self, other_component))
