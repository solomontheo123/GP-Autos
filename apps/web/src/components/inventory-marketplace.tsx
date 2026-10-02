"use client";

import { useMemo, useState } from "react";
import { VehicleCard } from "@/components/vehicle-card";
import type { Vehicle } from "@/lib/vehicles";

export function InventoryMarketplace({ initialVehicles }: { initialVehicles: Vehicle[] }) {
  const [query, setQuery] = useState("");
  const [make, setMake] = useState("all");
  const [condition, setCondition] = useState("all");
  const [sort, setSort] = useState("featured");

  const makeOptions = ["all", ...new Set(initialVehicles.map((vehicle) => vehicle.make))];
  const conditionOptions = ["all", ...new Set(initialVehicles.map((vehicle) => vehicle.condition))];

  const filteredVehicles = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();
    const list = initialVehicles.filter((vehicle) => {
      const matchesQuery =
        normalizedQuery.length === 0 ||
        [vehicle.title, vehicle.make, vehicle.model, vehicle.year.toString(), vehicle.location]
          .join(" ")
          .toLowerCase()
          .includes(normalizedQuery);

      const matchesMake = make === "all" || vehicle.make === make;
      const matchesCondition = condition === "all" || vehicle.condition === condition;

      return matchesQuery && matchesMake && matchesCondition;
    });

    switch (sort) {
      case "price-low":
        return [...list].sort((a, b) => a.price - b.price);
      case "price-high":
        return [...list].sort((a, b) => b.price - a.price);
      case "year-newest":
        return [...list].sort((a, b) => b.year - a.year);
      case "year-oldest":
        return [...list].sort((a, b) => a.year - b.year);
      default:
        return list;
    }
  }, [condition, initialVehicles, make, query, sort]);

  const clearFilters = () => {
    setQuery("");
    setMake("all");
    setCondition("all");
    setSort("featured");
  };

  return (
    <section className="listing-wrap">
      <div className="inventory-toolbar">
        <label className="inventory-search" aria-label="Search vehicles">
          <span aria-hidden="true">⌕</span>
          <input
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search vehicles..."
          />
          {query ? (
            <button type="button" onClick={() => setQuery("")} aria-label="Clear search">
              Clear
            </button>
          ) : null}
        </label>

        <div className="inventory-controls">
          <label>
            <span>Make</span>
            <select value={make} onChange={(event) => setMake(event.target.value)}>
              {makeOptions.map((option) => (
                <option key={option} value={option}>
                  {option === "all" ? "All makes" : option}
                </option>
              ))}
            </select>
          </label>

          <label>
            <span>Condition</span>
            <select value={condition} onChange={(event) => setCondition(event.target.value)}>
              {conditionOptions.map((option) => (
                <option key={option} value={option}>
                  {option === "all" ? "All conditions" : option}
                </option>
              ))}
            </select>
          </label>

          <label>
            <span>Sort</span>
            <select value={sort} onChange={(event) => setSort(event.target.value)}>
              <option value="featured">Featured</option>
              <option value="price-low">Price: low to high</option>
              <option value="price-high">Price: high to low</option>
              <option value="year-newest">Year: newest</option>
              <option value="year-oldest">Year: oldest</option>
            </select>
          </label>
        </div>
      </div>

      <div className="listing-toolbar listing-toolbar-compact">
        <span>
          {filteredVehicles.length} vehicle{filteredVehicles.length === 1 ? "" : "s"}
        </span>
        <button type="button" className="clear-button" onClick={clearFilters}>
          Clear filters
        </button>
      </div>

      {filteredVehicles.length === 0 ? (
        <section className="empty-state inset-empty-state">
          <h2>No vehicles match your search.</h2>
          <p>Try adjusting your filters or clearing the search to see the full GP Autos collection.</p>
          <button type="button" className="button button-dark" onClick={clearFilters}>Clear filters</button>
        </section>
      ) : (
        <div className="vehicle-grid">{filteredVehicles.map((vehicle) => <VehicleCard key={vehicle.id} vehicle={vehicle} />)}</div>
      )}
    </section>
  );
}
