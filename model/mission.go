package model

import (
	"database/sql"
	"time"

	"github.com/google/uuid"
)

type MissionStage int8

const (
	Planning MissionStage = iota
	Sourcing
	InProgress
	Complete
	Aborted
)

func (ms MissionStage) String() string {
	return [...]string{"Planning", "Sourcing", "In Progress", "Complete", "Aborted"}[ms]
}

type AssetClass int8

const (
	C AssetClass = iota
	B
	A
	S
)

func (ac AssetClass) String() string {
	return [...]string{"C", "B", "A", "S"}[ac]
}

type StarColor int8

const (
	Yellow StarColor = iota
	Red
	Blue
	Green
)

func (sc StarColor) String() string {
	return [...]string{"Yellow", "Red", "Blue", "Green"}[sc]
}

// Base contains common columns for all tables.
type DBBaseModel struct {
	ID        uuid.UUID `gorm:"type:uuid;primaryKey;default:(gen_random_uuid())"`
	CreatedAt time.Time
	UpdatedAt time.Time
	DeletedAt *time.Time `sql:"index"`
}

type ListItem struct {
	Description string
	Completed   bool
}

type Mission struct {
	DBBaseModel
	Codename    string `gorm:"unique"`
	Description sql.NullString
	StartDate   sql.NullTime
	EndDate     sql.NullTime
	Stage       MissionStage `gorm:"default:0"`
	Milestones  []ListItem   `gorm:"serializer:json"`
	Swag        []ListItem   `gorm:"serializer:json"`
	Tech        []ListItem   `gorm:"serializer:json"`
	Resources   []ListItem   `gorm:"serializer:json"`
	Log         []MissionLogEntry
	Media       []string `gorm:"serializer:json"`
}

type System struct {
	DBBaseModel
	Galaxy       string
	Region       sql.NullString
	System       sql.NullString
	Civilization sql.NullString
	StarColor    *StarColor
	BlackHole    bool
	Atlas        bool
	Outlaw       bool
}

type Planet struct {
	DBBaseModel
	SystemID     uuid.UUID
	Name         string
	Type         sql.NullString
	Alias        sql.NullString
	PortalCoords []int8   `gorm:"serializer:json"`
	Resources    []string `gorm:"serializer:json"`
	Ecosystem    []string `gorm:"serializer:json"`
	Description  string
	Dissonant    bool
	Media        []string `gorm:"serializer:json"`
}

type MissionLogEntry struct {
	DBBaseModel
	MissionID uuid.UUID
	Entry     string
	SystemID  *uuid.UUID
	PlanetID  *uuid.UUID
	BaseID    *uuid.UUID
	Media     []string `gorm:"serializer:json"`
}

type Discovery struct {
	DBBaseModel
	SystemID    *uuid.UUID
	PlanetID    *uuid.UUID
	Description string
	Wonder      bool
	Media       []string `gorm:"serializer:json"`
}

type Base struct {
	DBBaseModel
	PlanetID    *uuid.UUID
	BaseName    string
	BaseType    sql.NullString
	Description sql.NullString
	Ammenities  []string `gorm:"serializer:json"`
	Resources   []string `gorm:"serializer:json"`
	Media       []string `gorm:"serializer:json"`
}

func NewNullString(s string) sql.NullString {
	return sql.NullString{String: s, Valid: true}
}
